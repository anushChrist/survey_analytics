import uuid
import random
import streamlit as st
import pandas as pd
from pymongo import MongoClient
import numpy as np

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string
db = client["survey_db"]  # Replace with your database name
collection = db["survey_responses"]  # Replace with your collection name

def noise(p):
    return random.uniform(-abs(p), p)  # Introduce random noise between -1 and 1

# Function to generate sample data
def generate_sample_data(num_samples):
    data = []

    for _ in range(num_samples):
        token = str(uuid.uuid4())
        
        age = max(18, min(40, round(np.random.normal(24) + noise(3))))
        
        gender = random.choices(["Male", "Female", "Non-binary", "Prefer not to say"], weights=[0.4, 0.4, 0.1, 0.1])[0]  # Weighted random choice
        academic_program = random.choices(["Bachelors", "Masters", "Doctorate"], weights=[0.6, 0.3, 0.1])[0]
        year_of_study = random.choices(["1st year", "2nd Year", "3rd Year", "4th Year", "5th Year"], weights=[0.3, 0.3, 0.2, 0.1, 0.1])[0]
        
        # Generate GPA with a controlled non-uniform relationship with happiness
        happiness_rating = max(1, min(5, round(np.random.normal(3, 1) + noise(1))))  # Clamp and round to the nearest integer
       
        balance_contribution = max(1, min(5, round(np.random.normal(3, 1) + noise(1))))
        extra_curricular_happiness = max(1, min(5, round(np.random.normal(3, 1) + noise(2))))        
        procrastination = max(1, min(5, round(np.random.normal(4, 1) + noise(1))))

        work_life_balance =  max(1, min(5, round(np.mean(np.random.normal(2, 1) + noise(1) + balance_contribution - (2*procrastination) + extra_curricular_happiness))))

        study_habits = max(1, min(5, round(np.mean(np.random.normal(3, 1) + noise(2) + work_life_balance - procrastination))))
        

        study_hours = max(1, min(10, round(study_habits + noise(3))))  
        scaled_study_hours = (study_hours / 2)

        class_attendance = random.choices(["Never", "Rarely", "Sometimes", "Often"], weights=[0.2, 0.3, 0.3, 0.2])[0]  # Weighted random choice
        attendance_mapping = {"Never": 4, "Rarely": 3, "Sometimes": 2,"Often": 1}
        num_class_attendance = attendance_mapping[class_attendance] / 4 * 5

        
        
        academic_impact = max(1, min(5, round(np.random.normal(3, 1) + noise(1))))  # Normal distribution with a mean of 3

        academic_pressure = max(1, min(5, round(academic_impact + noise(1.5))))  # Normal distribution with a mean of 3
        
        academic_guilt = max(1, min(5, round(academic_impact + noise(1))))
        happiness_factors = random.choices(["Family relationships", "Friendships", "Academic success", "Physical health", "Mental health", "Financial well-being", "Hobbies and interests", "Other"], weights=[0.1, 0.1, 0.2, 0.1, 0.2, 0.1, 0.1, 0.1])[0]
        
        
        

        gpa = max(1, min(5, round(np.mean(happiness_rating + study_habits + scaled_study_hours + num_class_attendance + academic_pressure + academic_impact - (3*procrastination)))))
        
        cheating_guilt = max(1, min(5, round(np.mean(np.random.normal(3, 1) + academic_guilt + noise(2)))))
        
        group_guilt = random.choices([1, 2, 3, 4, 5], weights=[0.3, 0.1, 0.1, 0.2, 0.3])[0]  # Weighted random choice
        
        attendance_impact = random.choices(["Positive", "Negative"], weights=[0.7, 0.3])[0]  # Weighted random choice
        
        additional_comments = ""

        response = {
            "token": token,
            "age": age,
            "gen": gender,
            "acad_prg": academic_program,
            "yo_stud": year_of_study,
            "gpa": gpa,
            "stud_hb": study_habits,
            "stud_hr": study_hours,
            "attend": class_attendance,
            "hap_rate": happiness_rating,
            "hap_fact": happiness_factors,
            "acad_impc": academic_impact,
            "acad_press": academic_pressure,
            "acad_guilt": academic_guilt,
            "bal_contri": balance_contribution,
            "proc": procrastination,
            "wl_bal": work_life_balance,
            "extra_curr_hap": extra_curricular_happiness,
            "ch_guilt": cheating_guilt,
            "gr_guilt": group_guilt,
            "attd_impc": attendance_impact,
            "add_comment": additional_comments
        }

        data.append(response)

    return data

# Streamlit user interface
st.title("Student Happiness and Academic Performance Survey Data Generator")
num_samples = st.number_input("Enter the number of samples you want to generate:", min_value=1, value=100)

if st.button("Generate and Insert Data"):
    sample_data = generate_sample_data(num_samples)
    collection.insert_many(sample_data)
    st.success(f"Inserted {num_samples} sample records into the MongoDB database.")

st.write("This app generates sample data for a student survey with non-uniform, right-skewed distributions.")
