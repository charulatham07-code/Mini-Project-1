# ---------------------------------------------------------------
# This file reads your CSV and inserts the data into MySQL table.
# It is intended to be run ONCE.
# ---------------------------------------------------------------

import pandas as pd
from datetime import datetime
from config.db_config import get_connection

CSV_PATH = "E:/DS_Projects/Client_Query_management/data/synthetic_client_queries.csv"

def upload_csv_to_database():
    # Read CSV
    df = pd.read_csv(CSV_PATH)

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO client_queries
        (email, mobile, query_heading, query_description, 
         query_created_time, status, query_closed_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    rows_inserted = 0

    for _, row in df.iterrows():

        # Convert dates
        created_time = datetime.strptime(row["date_raised"], "%Y-%m-%d")
        closed_time = None
        if isinstance(row["date_closed"], str) and row["date_closed"].strip() != "":
            closed_time = datetime.strptime(row["date_closed"], "%Y-%m-%d")

        cursor.execute(insert_query, (
            row["client_email"],
            str(row["client_mobile"]),
            row["query_heading"],
            row["query_description"],
            created_time,
            row["status"],
            closed_time
        ))

        rows_inserted += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Upload Complete! {rows_inserted} rows inserted successfully.")

if __name__ == "__main__":
    upload_csv_to_database()
