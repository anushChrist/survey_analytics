# survey.py
import streamlit as st
import pandas as pd
import uuid

def susu(collection):
    """# Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["survey_db"]
    collection = db["survey_responses"]"""

    # Create the survey form
    st.title("Student Happiness and Academic Performance Survey")

    # Demographic Information
    age = st.number_input("1. Age:")
    gender = st.selectbox("2. Gender:", ["Male", "Female", "Non-binary", "Prefer not to say"])
    academic_program = st.selectbox("3. Academic Program:", ["Bachelors", "Masters", "Doctorate"])
    year_of_study = st.selectbox("4. Year of Study:", ["1st year", "2nd Year", "3rd Year", "4th Year", "5th Year"])

    # Academic Performance
    gpa = st.slider("5. On a scale of 1 to 5, rate your academic performance:", 1, 5)
    study_habits = st.slider("6. On a scale of 1 to 5, rate your study habits:", 1, 5)
    study_hours = st.number_input("7. On average, how many hours do you study per day?")
    class_attendance = st.selectbox("8. How often do you miss classes?", ["Never", "Rarely", "Sometimes", "Often"])

    # Overall Happiness/Quality of Life
    happiness_rating = st.slider("9. On a scale of 1 to 5, rate your overall happiness and quality of life:", 1, 5)
    happiness_factors = st.selectbox("10. What factors contribute most to your happiness and quality of life?", ["Family relationships", "Friendships", "Academic success", "Physical health", "Mental health", "Financial well-being", "Hobbies and interests", "Other"])

    # Relationship between Happiness and Academic Performance
    academic_impact = st.slider("11. On a scale of 1 to 5, to what extent do you think that your academic performance has an impact on your overall happiness?", 1, 5)
    academic_pressure = st.slider("12. On a scale of 1 to 5, how much pressure do you feel to perform well academically?", 1, 5)
    academic_guilt = st.slider("13. On a scale of 1 to 5, how guilty do you feel when you fail to perfom well in your adademics?", 1, 5)
    balance_contribution = st.slider("14. On a scale of 1 to 5, do you think that achieving a balance between academic commitments and personal life contributes to your happiness and quality of life?", 1, 5)
    procrastination = st.slider("15. On a scale of 1 to 5, how much do you tend to procrastinate?", 1, 5)
    extra_curricular_happiness = st.slider("16. On a scale of 1 to 5, do you think engaging in extra-curricular activities makes you happy outside your academic responsibilities?", 1, 5)
    work_life_balance = st.slider("17. On a scale of 1 to 5, how well do you think you manage you work-life balance?", 1, 5)
    cheating_guilt = st.slider("18. On a scale of 1 to 5, how guilty do you feel when you score well after cheating in your exams?", 1, 5)
    group_guilt = st.slider("19. On a scale of 1 to 5, how guilty do you feel when you get credit for a group project even tho you contributed nothing to it?", 1, 5)
    attendance_impact = st.selectbox("20. What impact has mandatory attendance had on your academic performace?", ["Positive", "Negative"])

    # Additional Comments
    additional_comments = st.text_area("21. Do you have any additional comments or insights on the relationship between academic performance and overall happiness that you would like to share?")

    if st.button("Submit"):
        # Generate a unique token
        token = str(uuid.uuid4())
        
        # Store survey responses with the token in MongoDB
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
        collection.insert_one(response)
        st.success("Survey response submitted successfully! Please save this token for future use incase you wish to update/delete your preferences.")
        st.success(f"{token}")