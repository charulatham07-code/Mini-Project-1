import streamlit as st
from pages.login_page import login_page
from pages.register_page import registration_page
from pages.client_page import client_screen
from pages.support_page import support_screen
from user_function.logo_display import login_display


# ---------------------------
# Basic Page Config
# ---------------------------

st.set_page_config(
    page_title="Client Query Management System",
    layout="wide"  # allows left + right alignment

)

# ---------------------------
# Remove Streamlit default hamburger menu & footer
# ---------------------------
hide_menu_css = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_css, unsafe_allow_html=True)


# ---------------------------
# Initialize session state
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_login" not in st.session_state:
    st.session_state.show_login = False  # default → show register first

# ---------------------------
# Routing Logic
# ---------------------------
if not st.session_state.logged_in:
    
    # Show header/logo only on login/register
    login_display()


    # ---------------------------
    # SHOW REGISTER FIRST
    # ---------------------------
    if not st.session_state.show_login:
        st.info("New User? Register Below")

        registration_page()

        st.info("Already registered? Click the below to login.")

        if st.button("***Go to Login →***"):
            st.session_state.show_login = True
            st.rerun()

    # ---------------------------
    # SHOW LOGIN PAGE
    # ---------------------------
    else:
        st.info("Existing User! Please proceed with Login")

        login_page()

        st.info("New user? Click below to create an account.")

        if st.button("***← Go to Register***"):
            st.session_state.show_login = False
            st.rerun()

# ---------------------------
# AFTER LOGIN → SHOW ROLE PAGES
# ---------------------------
else:
    # Hide the button-like elements used earlier
    st.empty()

    # Client Page
    if st.session_state.role == "client":
        client_screen()

    # Support Page
    elif st.session_state.role == "support":
        support_screen()

    # Logout button
    if st.button("***Logout***"):
        st.session_state.logged_in = False
        st.session_state.show_login = False
        st.rerun()


