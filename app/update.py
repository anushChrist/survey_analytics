# update.py
import streamlit as st


def update(collection):

    st.title("Update Records")

    # Input field for token
    token = st.text_input("Enter Token:")
    # Demographic Information
    new_age = st.number_input("1. Age:",min_value=18, max_value=50,step=1)
    new_gender = st.selectbox("2. Gender:", ["Male", "Female", "Non-binary", "Prefer not to say"])
    new_academic_program = st.selectbox("3. Academic Program:", ["Bachelors", "Masters", "Doctorate"])
    new_year_of_study = st.selectbox("4. Year of Study:", ["1st year", "2nd Year", "3rd Year", "4th Year", "5th Year"])

    # Academic Performance
    new_gpa = st.slider("5. On a scale of 1 to 5, rate your academic performance:", 1, 5)
    new_study_habits = st.slider("6. On a scale of 1 to 5, rate your study habits:", 1, 5)
    new_study_hours = st.number_input("7. On average, how many hours do you study per day?")
    new_class_attendance = st.selectbox("8. How often do you miss classes?", ["Never", "Rarely", "Sometimes", "Often"])

    # Overall Happiness/Quality of Life
    new_happiness_rating = st.slider("9. On a scale of 1 to 5, rate your overall happiness and quality of life:", 1, 5)
    new_happiness_factors = st.selectbox("10. What factors contribute most to your happiness and quality of life?", ["Family relationships", "Friendships", "Academic success", "Physical health", "Mental health", "Financial well-being", "Hobbies and interests", "Other"])

    # Relationship between Happiness and Academic Performance
    new_academic_impact = st.slider("11. On a scale of 1 to 5, to what extent do you think that your academic performance has an impact on your overall happiness?", 1, 5)
    new_academic_pressure = st.slider("12. On a scale of 1 to 5, how much pressure do you feel to perform well academically?", 1, 5)
    new_academic_guilt = st.slider("13. On a scale of 1 to 5, how guilty do you feel when you fail to perfom well in your adademics?", 1, 5)
    new_balance_contribution = st.slider("14. On a scale of 1 to 5, do you think that achieving a balance between academic commitments and personal life contributes to your happiness and quality of life?", 1, 5)
    new_procrastination = st.slider("15. On a scale of 1 to 5, how much do you tend to procrastinate?", 1, 5)
    new_extra_curricular_happiness = st.slider("16. On a scale of 1 to 5, do you think engaging in extra-curricular activities makes you happy outside your academic responsibilities?", 1, 5)
    new_work_life_balance = st.slider("17. On a scale of 1 to 5, how well do you think you manage you work-life balance?", 1, 5)
    new_cheating_guilt = st.slider("18. On a scale of 1 to 5, how guilty do you feel when you score well after cheating in your exams?", 1, 5)
    new_group_guilt = st.slider("19. On a scale of 1 to 5, how guilty do you feel when you get credit for a group project even tho you contributed nothing to it?", 1, 5)
    new_attendance_impact = st.selectbox("20. What impact has mandatory attendance had on your academic performace?", ["Positive", "Negative"])

    # Additional Comments
    new_additional_comments = st.text_area("21. Do you have any additional comments or insights on the relationship between academic performance and overall happiness that you would like to share?")
    
    if st.button("Confirm Update"):
        record = collection.find_one({"token": token})
        if record:
            collection.update_one(
                    {"token": token},
                    {"$set": {"token": token, 
                                "age": new_age,
                                "gen": new_gender,
                                "acad_prg": new_academic_program,
                                "yo_stud": new_year_of_study,
                                "gpa": new_gpa,
                                "stud_hb": new_study_habits,
                                "stud_hr": new_study_hours,
                                "attend": new_class_attendance,
                                "hap_rate": new_happiness_rating,
                                "hap_fact": new_happiness_factors,
                                "acad_impc": new_academic_impact,
                                "acad_press": new_academic_pressure,
                                "acad_guilt": new_academic_guilt,
                                "bal_contri": new_balance_contribution,
                                "proc": new_procrastination,
                                "wl_bal": new_work_life_balance,
                                "extra_curr_hap": new_extra_curricular_happiness,
                                "ch_guilt": new_cheating_guilt,
                                "gr_guilt": new_group_guilt,
                                "attd_impc": new_attendance_impact,
                                "add_comment": new_additional_comments}}
                )
            st.success("Record updated successfully.")
        else:
            st.warning("Record not found.")