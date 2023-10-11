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
    survey.susu(collection)
elif selected_option == "Analytics":
    analytics.anal(collection)
elif selected_option == "Show":
    show.didi(collection)
elif selected_option == "Delete":
    delete.dudu(collection)
elif selected_option == "Update":
    update.pupu(collection)
