# app.py
import streamlit as st
import pymongo
import survey
import analytics
import delete
import update
import show

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["survey_db"]
collection = db["survey_responses"]

# Sidebar navigation
st.sidebar.title("Navigation")
selected_option = st.sidebar.radio("Select Option", ["Survey", "Analytics", "Show", "Update", "Delete"])

if selected_option == "Survey":
    survey.survey(collection)
elif selected_option == "Analytics":
    analytics.analytics(collection)
elif selected_option == "Show":
    show.show(collection)
elif selected_option == "Delete":
    delete.delete(collection)
elif selected_option == "Update":
    update.update(collection)
