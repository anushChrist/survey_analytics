# delete_update.py
import streamlit as st
import pymongo

def dudu():
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["survey_db"]
    collection = db["survey_responses"]

    st.title("Delete/Update Records")

    # Input field for token
    token = st.text_input("Enter Token:")

    # Display record for the entered token
    if st.button("Show Record"):
        record = collection.find_one({"token": token})
        if record:
            st.subheader("Survey Response")
            st.write(record)
        else:
            st.warning("Record not found.")

    # Delete record for the entered token
    if st.button("Delete Record"):
        deleted_record = collection.delete_one({"token": token})
        if deleted_record.deleted_count > 0:
            st.success("Record deleted successfully.")
        else:
            st.warning("Record not found.")

    # Update record for the entered token
    if st.button("Update Record"):
        record = collection.find_one({"token": token})
        if record:
            st.subheader("Update Survey Response")
            new_rating = st.slider("Update Rating (1-5):", 1, 5, record["rating"])
            new_comments = st.text_area("Update Comments:", record["comments"])
            
            # Update the record
            collection.update_one(
                {"token": token},
                {"$set": {"rating": new_rating, "comments": new_comments}}
            )
            st.success("Record updated successfully.")
        else:
            st.warning("Record not found.")
