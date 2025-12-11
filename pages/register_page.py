# This file contains the registration user interface.

import streamlit as st
from database.db import insert_user
from auth.hashing import hash_password
from database.db import get_user_by_username
from user_function.validate import validate_email, validate_password

def registration_page():
    st.subheader("Create a New Account")

    if "reg_confirm_password" not in st.session_state:
        st.session_state.reg_confirm_password = ""

    # STEP 1: Clear logic BEFORE widgets render ---
    if "clear_form" not in st.session_state:
        st.session_state.clear_form = False

    if "registration_success" not in st.session_state:
        st.session_state.registration_success = False

    if st.session_state.clear_form:
        st.session_state.reg_username = ""
        st.session_state.reg_password = ""
        st.session_state.reg_confirm_password = ""
        st.session_state.reg_role = "Select Role"
        st.session_state.clear_form = False

    username = st.text_input("***Email ID***", key="reg_username")
    password = st.text_input("***Password***", type="password", key= "reg_password")
    confirm_password = st.text_input("***Confirm Password***", type="password", key="reg_confirm_password")
    options = ["Select Role", "client", "support"]
    role = st.selectbox("***Choose a role***", options, key="reg_role")

     # Register button clicked
    if st.button("***Register***"):
        # Validation and checking
        
        # Checks the input fields is not empty
        if not username:
            st.warning("Email ID cannot be empty!")
            return
        
        # Checks the entered email ID is valid
        if not validate_email(username):
            st.error("Invalid email! Please enter a valid email ID (example: name@example.com).")
            return

        # Check if username already exists
        existing_user = get_user_by_username(username)
        if existing_user:
            st.error("This user already exists. Please proceed to login.")
            return

        
        # Checks the input fields is not empty
        if not password:
            st.warning("Password cannot be empty!")
            return

        # Checks the entered password is valid
        if not validate_password(password):
            st.error(
                "Weak password! Password must include:\n"
                "- Minimum 8 characters\n"
                "- At least 1 uppercase letter\n"
                "- At least 1 lowercase letter\n"
                "- At least 1 number\n"
                "- At least 1 special character (@#$%^&+=!)"
            )
            return
        
        if not confirm_password:
            st.warning("Confirm Password cannot be empty!")
            return
        
        # Check if passwords match
        if password != confirm_password:
            st.error("Passwords do not match. Please re-enter.")
            return
        
        # Checks the user has entered a valid role 
        if role == "Select Role":
            st.warning("Please choose a valid role!")
            return

        # Hash password and insert in DB
        hashed_pw = hash_password(password)
        insert_user(username, hashed_pw, role)

        # Flag for form clearing + success message
        st.session_state.clear_form = True
        st.session_state.registration_success = True

        st.rerun()   # restart script immediately

    # -------------------------------
    # SHOW SUCCESS MESSAGE AFTER RERUN
    # -------------------------------
    if st.session_state.registration_success:
        st.success("Registration Successful! Please proceed with Login.")
        st.session_state.registration_success = False
        
