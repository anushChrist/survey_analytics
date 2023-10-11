import streamlit as st
import uuid
import pymongo
import random

# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["survey_db"]
collection = db["survey_responses"]

# Function to generate random data
def generate_random_data():
    age = random.randint(18, 35)
    gender = random.choice(["Male", "Female", "Non-binary", "Prefer not to say"])
    academic_program = random.choice(["Bachelors", "Masters", "Doctorate"])
    year_of_study = random.choice(["1st year", "2nd Year", "3rd Year", "4th Year", "5th Year"])
    gpa = random.randint(1, 5)
    study_habits = random.randint(1, 5)
    study_hours = random.randint(1, 10)  # Adjust the range as needed
    class_attendance = random.choice(["Never", "Rarely", "Sometimes", "Often"])
    happiness_rating = random.randint(1, 5)
    happiness_factors = random.choice(["Family relationships", "Friendships", "Academic success", "Physical health", "Mental health", "Financial well-being", "Hobbies and interests", "Other"])
    academic_impact = random.randint(1, 5)
    academic_pressure = random.randint(1, 5)
    academic_guilt = random.randint(1, 5)
    balance_contribution = random.randint(1, 5)
    procrastination = random.randint(1, 5)
    extra_curricular_happiness = random.randint(1, 5)
    work_life_balance = random.randint(1, 5)
    cheating_guilt = random.randint(1, 5)
    group_guilt = random.randint(1, 5)
    attendance_impact = random.choice(["Positive", "Negative"])
    additional_comments = ""

    return {
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

# Streamlit UI
st.title("Generate Random Survey Data")
number_of_samples = st.number_input("Number of samples to generate:", min_value=1, step=1)
if st.button("Generate and Insert"):
    for _ in range(number_of_samples):
        token = str(uuid.uuid4())
        response_data = generate_random_data()
        response_data["token"] = token
        collection.insert_one(response_data)
        st.write(f"Survey response with token {token} inserted successfully!")

# Close the MongoDB connection
client.close()
