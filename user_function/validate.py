import re
import streamlit as st


def validate_email(username):
    # Strict email validation
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, username) is not None

def validate_emailID(email):
    # Strict email validation
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, email) is not None

def validate_password(password):
    # At least 8 chars, 1 upper, 1 lower, 1 digit, 1 special char
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
    return re.fullmatch(pattern, password) is not None

