# analytics.py
import streamlit as st
import pandas as pd



# Connect to MongoDB
def anal(collection):

    survey_data = pd.DataFrame(list(collection.find()))
    st.title("Analytics")

    # Summary statistics
    st.header("Summary Statistics")
    st.write(survey_data.describe())

    # Distribution of Age
    st.header("Age Distribution")
    st.bar_chart(survey_data['age'].value_counts())

    # Gender Distribution
    st.header("Gender Distribution")
    st.bar_chart(survey_data['gen'].value_counts())

    # Academic Program Distribution
    st.header("Academic Program Distribution")
    st.bar_chart(survey_data['acad_prg'].value_counts())