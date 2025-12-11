# This file contains the login user interface.
# It uses Streamlit text boxes and buttons.

import streamlit as st
from database.db import validate_user
from auth.hashing import hash_password


def login_page():
    st.subheader("Login to Your Account")

    username = st.text_input("***Email ID***")
    password = st.text_input("***Password***", type="password")

    # Login button clicked
    if st.button("***Login***"):

        # Input validation
        if not username:
            st.warning("Please enter your Register Email ID!")
            return
        if not password:
            st.warning("Please enter your password!")
            return
        
        # Hash the entered password and check match
        hashed_pw = hash_password(password)
        user = validate_user(username, hashed_pw)

        if user:
            # Save login details in Streamlit session
            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]
            st.rerun()

        else:
            st.error("Incorrect Email ID or Password")
        
        
