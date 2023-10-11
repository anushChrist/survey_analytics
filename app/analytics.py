# analytics.py
import streamlit as st
import pandas as pd

# Connect to MongoDB
def anal(collection):
    """client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["survey_db"]
    collection = db["survey_responses"]"""

    # Analyze survey data
    st.title("Survey Analytics")

    # Fetch survey data from MongoDB
    responses = list(collection.find())
    if responses:
        df = pd.DataFrame(responses)

        st.subheader("Response Distribution")
        st.bar_chart(df["rating"].value_counts())

        st.subheader("Comments Word Cloud")
        # Implement word cloud generation using a library like wordcloud

        # You can also add more analytics as needed

    else:
        st.warning("No survey responses yet.")
