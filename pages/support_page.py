import streamlit as st
import pandas as pd
from datetime import datetime, date

from database.db import update_query_status, get_all_queries
from user_function.logo_display import support_display


def support_screen():

    support_display()
    st.info("You can view, filter, and close client queries in real-time.")

    # LOAD ALL QUERIES
    try:
        rows = get_all_queries()
        df = pd.DataFrame(rows)
    except Exception as e:
        st.error(f"Error loading queries from database: {e}")
        return

    if df.empty:
        st.warning("No queries found.")
        return

    # FORMAT DATE COLUMNS
    df["query_created_time"] = pd.to_datetime(df["query_created_time"])
    df["query_closed_time"] = pd.to_datetime(df["query_closed_time"], errors='coerce')

    # TIME TAKEN CALCULATION
    def format_time_fixed(hours):
        if pd.isna(hours):
            return "-"
        total_minutes = int(hours * 60)
        days = total_minutes // (24*60)
        hours_part = (total_minutes % (24*60)) // 60
        minutes = total_minutes % 60
        return f"{days}d {hours_part}h {minutes}m"

    df["Time Taken"] = (
        (df["query_closed_time"] - df["query_created_time"]).dt.total_seconds() / 3600
    ).apply(format_time_fixed)

    # SERVICE METRICS
    open_queries = df[df["status"].str.lower().isin(["open", "opened"])]
    closed_queries = df[df["status"].str.lower() == "closed"]

    today = date.today()

    closed_today = closed_queries[
        closed_queries["query_closed_time"].dt.date == today
    ].shape[0]

    submitted_today = df[
        df["query_created_time"].dt.date == today
    ].shape[0]

    st.subheader("***Service Efficiency***")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Queries", df.shape[0])
    col2.metric("Closed", closed_queries.shape[0])
    col3.metric("Open", open_queries.shape[0])
    col4.metric("Submitted Today", submitted_today)
    col5.metric("Closed Today", closed_today)

    # FILTER SECTION
    st.subheader("***Filter Queries***")

    if "search_text" not in st.session_state:
        st.session_state.search_text = ""

    def clear_search():
        st.session_state.search_text = ""

    filter_category = st.selectbox(
        "Select Category:",
        ["None", "email", "mobile", "query_heading", "status"],
        key="category",
        on_change=clear_search
    )

    search_text = ""
    status_filter = "All"

    if filter_category == "status":
        status_filter = st.selectbox("Select Status:", ["All", "Open", "Closed"], key="status_filter")
    elif filter_category != "None":
        search_text = st.text_input("Enter text to filter:", key="search_text")

    filtered_df = df.copy()

    if filter_category == "status":
        if status_filter != "All":
            if status_filter.lower() == "open":
                filtered_df = filtered_df[filtered_df["status"].str.lower().isin(["open", "opened"])]
            else:
                filtered_df = filtered_df[filtered_df["status"].str.lower() == "closed"]

    elif filter_category != "None" and search_text.strip():
        filtered_df = filtered_df[
            filtered_df[filter_category].astype(str).str.contains(search_text.strip(), case=False, na=False)
        ]

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # CLOSE QUERY SECTION
    st.write("----")
    st.subheader("***Close an Open Query***")

    if "close_message" in st.session_state:
        st.success(st.session_state.close_message)
        del st.session_state.close_message

    if open_queries.empty:
        st.success("All queries are closed!")
    else:
        query_options = ["Select a Query"] + open_queries["query_id"].tolist()
        selected_query_id = st.selectbox("Select an Open Query:", query_options)

        if selected_query_id != "Select a Query":
            selected_query = open_queries[open_queries["query_id"] == selected_query_id]
            st.write("***Query Details***")
            st.dataframe(selected_query, use_container_width=True, hide_index=True)

            closing_comment = st.text_area("Add closing comment before closing:", key="closing_comment")

            if st.button("***Close This Query***"):
                if not closing_comment.strip():
                    st.warning("Closing comment is required!")
                else:
                    try:
                        closed_time = datetime.now()
                        update_query_status(
                            selected_query_id,
                            "Closed",
                            closed_time,
                            closing_comment
                        )
                        st.session_state.close_message = f"Query {selected_query_id} closed successfully!"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error closing query: {e}")

    # --------------------------
    # SUPPORT LOAD MONITORING 
    # --------------------------
    st.write("---")
    st.subheader("***Support Load Monitoring***")

    try:
        # Most Common Queries: total count per category
        common_queries_df = df.groupby("query_heading").agg(
            Total_Queries=("query_id", "count")
        ).reset_index().rename(columns={"query_heading": "Category"}).sort_values(by="Total_Queries", ascending=False)

        st.write("***Most Common Queries***")
        st.dataframe(common_queries_df, use_container_width=True, hide_index=True)

        # Backlog: number of open queries per category
        backlog_df = df[df["status"].str.lower().isin(["open", "opened"])].groupby("query_heading").agg(
            Open_Queries=("query_id", "count")
        ).reset_index().rename(columns={"query_heading": "Category"}).sort_values(by="Open_Queries", ascending=False)

        st.write("***Backlog - Open Queries***")
        st.dataframe(backlog_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Failed to calculate load metrics: {e}")
