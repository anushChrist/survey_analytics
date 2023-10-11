# show.py
import streamlit as st

def didi(collection):
    st.title("Display Record")
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