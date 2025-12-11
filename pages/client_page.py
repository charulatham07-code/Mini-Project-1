# Client Page: client_screen.py
import streamlit as st
from datetime import datetime
from user_function.logo_display import client_display
from user_function.validate import validate_emailID
from database.db import insert_client_query, fetch_queries_by_email

def client_screen():
    # Display logo or header
    client_display()

    st.subheader("***Submit Your Query***")
    st.info("All fields are mandatory to submit a query!!")

    # ---------------------------------------
    # SESSION STATE INITIALIZATION
    # ---------------------------------------
    if "clear_query" not in st.session_state:
        st.session_state.clear_query = False

    if "query_success" not in st.session_state:
        st.session_state.query_success = False

    # Preserve form inputs
    for key in ["EmailID", "Mobile", "Query_Heading", "Query_Description"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    # Preserve history email input
    if "history_email" not in st.session_state:
        st.session_state.history_email = ""

    # Clear form input fields after successful submission
    if st.session_state.clear_query:
        st.session_state.EmailID = ""
        st.session_state.Mobile = ""
        st.session_state.Query_Heading = "Select a Option"
        st.session_state.Query_Description = ""
        st.session_state.clear_query = False

    # ---------------------------------------
    # INPUT FIELDS - QUERY FORM
    # ---------------------------------------
    email = st.text_input("***Email ID***", key="EmailID")
    mobile = st.text_input("***Mobile Number***", key="Mobile")

    option = [
        "Select a Option", "UI Feedback", "Feature Request", "Payment Failure",
        "Subscription Cancellation", "Technical Support", "Account Suspension",
        "Billing Problem", "Bug Report", "Data Export", "Others"
    ]
    query_heading = st.selectbox("***Query Title***", option, key="Query_Heading")
    query_description = st.text_area("***Query Description***", height=150, key="Query_Description")

    # ---------------------------------------
    # SUBMIT QUERY BUTTON
    # ---------------------------------------
    if st.button("***Submit Query***"):
        # --- INPUT VALIDATIONS ---
        if not email:
            st.warning("Email ID cannot be empty!")
        elif not validate_emailID(email):
            st.error("Invalid email ID! Example: name@example.com")
        elif not mobile:
            st.warning("Mobile Number cannot be empty!")
        elif not mobile.isdigit() or len(mobile) != 10:
            st.error("Mobile number must be exactly 10 digits.")
        elif query_heading == "Select a Option":
            st.warning("Please choose a valid Query Title!")
        elif not query_description:
            st.warning("Query Description cannot be empty!")
        else:
            # Valid input - insert into DB
            query_created_time = datetime.now()
            status = "Open"
            try:
                insert_client_query(
                    email,
                    mobile,
                    query_heading,
                    query_description,
                    query_created_time,
                    status,
                    None  # query_closed_time
                )
                st.session_state.clear_query = True
                st.session_state.query_success = True
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    # ---------------------------------------
    # SUCCESS MESSAGE AFTER FORM SUBMISSION
    # ---------------------------------------
    if st.session_state.query_success:
        st.success("Query Submitted successfully!")
        st.session_state.query_success = False

    # ---------------------------------------
    # QUERY HISTORY SECTION
    # ---------------------------------------
    st.write("---")
    st.subheader("***Your Query History***")

    # Input field for history email
    st.text_input(
        "Enter your Email ID to view your query history",
        key="history_email"
    )
    history_email = st.session_state.history_email  # Use session state to persist value

    if history_email:
        try:
            df = fetch_queries_by_email(history_email)

            if df.empty:
                st.info("No queries found for this email.")
            else:
                display_df = df[[
                    "query_id",
                    "query_heading",
                    "query_description",
                    "query_created_time",
                    "status",
                    "closing_comment"
                ]].copy()

                display_df.rename(columns={
                    "closing_comment": "Support Closing Comment"
                }, inplace=True)

                st.dataframe(display_df, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Failed to load query history: {e}")
