# delete_update.py
import streamlit as st

def dudu(collection):
    # Connect to MongoDB
    """client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["survey_db"]
    collection = db["survey_responses"]"""

    st.title("Delete Records")

    # Input field for token
    token = st.text_input("Enter Token:")

    # Delete record for the entered token
    if st.button("Confirm Delete"):
        deleted_record = collection.delete_one({"token": token})
        if deleted_record.deleted_count > 0:
            st.success("Record deleted successfully.")
        else:
            st.warning("Record not found.")

    