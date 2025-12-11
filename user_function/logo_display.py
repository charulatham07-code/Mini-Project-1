import streamlit as st

# ---------------------------
# Load Logo Image (Right Corner) in Registration and Login screen
# ---------------------------

def login_display():

    col1, col2 = st.columns([7, 2])  # title left, logo right

    with col1:
        st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">
        <h1 style="
            text-align: left;
            color: green;
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            margin-top: 0px;
        ">
            Client Query Management System
        <br>
        </h1>
    """, unsafe_allow_html=True
    )
   
    with col2:
        st.image("images/new_logo.png", width=180)

# ---------------------------
# Load Logo Image (Right Corner) in client page
# ---------------------------

def client_display():
    col1, col2 = st.columns([7, 2])  # title left, logo right

    with col1:
        st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">
        <h1 style="
            text-align: left;
            color: green;
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            margin-top: 0px;
        ">
            Client - Query Portal
        </h1>
    """, unsafe_allow_html=True
    )
   
    with col2:
        st.image("images/new_logo.png", width=180)

# ---------------------------
# Load Logo Image (Right Corner) in support page
# ---------------------------

def support_display():
    col1, col2 = st.columns([7, 2])  # title left, logo right

    with col1:
        st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">
        <h1 style="
            text-align: left;
            color: green;
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            margin-top: 0px;
        ">
            Support Query Management Dashboard
        </h1>
    """, unsafe_allow_html=True
    )
   
    with col2:
        st.image("images/new_logo.png", width=180)




 

    

