# survey.py
import streamlit as st
import pymongo
import pandas as pd
import uuid

def susu():
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["survey_db"]
    collection = db["survey_responses"]

    # Create the survey form
    st.title("Survey Reporting Website")

    name = st.text_input("Name:")
    email = st.text_input("Email:")
    rating = st.slider("Rating (1-5):", 1, 5)
    comments = st.text_area("Comments:")

    if st.button("Submit"):
        # Generate a unique token
        token = str(uuid.uuid4())
        
        # Store survey responses with the token in MongoDB
        response = {
            "token": token,
            "name": name,
            "email": email,
            "rating": rating,
            "comments": comments,
        }
        collection.insert_one(response)
        st.success(f"Survey response submitted successfully! Token: {token}")
