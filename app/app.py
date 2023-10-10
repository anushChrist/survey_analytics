# app.py
import streamlit as st
import survey
import analytics
import delete_update

# Sidebar navigation
st.sidebar.title("Navigation")
selected_option = st.sidebar.radio("Select Option", ["Survey", "Analytics", "Delete/Update"])

if selected_option == "Survey":
    survey.susu()
elif selected_option == "Analytics":
    analytics.anal()
elif selected_option == "Delete/Update":
    delete_update.dudu()
