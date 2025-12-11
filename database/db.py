import pandas as pd
from config.db_config import get_connection


# ---------------------------------------------------
# INSERT NEW USER
# ---------------------------------------------------

def insert_user(username, hashed_password, role):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO users (username, hashed_password, role) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, hashed_password, role))

    conn.commit()
    cursor.close()
    conn.close()


# ---------------------------------------------------
# VALIDATE LOGIN USER
# ---------------------------------------------------

def validate_user(username, hashed_password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE username=%s AND hashed_password=%s"
    cursor.execute(query, (username, hashed_password,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user


# ---------------------------------------------------
# FETCH USER BY USERNAME
# ---------------------------------------------------

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    get_user = cursor.fetchone()

    cursor.close()
    conn.close()
    return get_user


# ---------------------------------------------------
# INSERT NEW CLIENT QUERY
# ---------------------------------------------------

def insert_client_query(email, mobile, query_heading, query_description, query_created_time, status, query_closed_time):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO client_queries
        (email, mobile, query_heading, query_description, query_created_time, status, query_closed_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        email, mobile, query_heading, query_description,
        query_created_time, status, query_closed_time
    ))

    conn.commit()
    cursor.close()
    conn.close()


# ---------------------------------------------------
# GET ALL CLIENT QUERIES (SUPPORT DASHBOARD)
# ---------------------------------------------------

def get_all_queries():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM client_queries ORDER BY query_created_time DESC"
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


# ---------------------------------------------------
# UPDATE QUERY STATUS + CLOSING COMMENT
# ---------------------------------------------------

def update_query_status(query_id, status, closed_time, closing_comment):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE client_queries 
        SET status = %s,
            query_closed_time = %s,
            closing_comment = %s
        WHERE query_id = %s
    """

    cursor.execute(query, (status, closed_time, closing_comment, query_id))

    conn.commit()
    cursor.close()
    conn.close()


# ---------------------------------------------------
# FETCH QUERY HISTORY FOR CLIENT PAGE
# ---------------------------------------------------

def fetch_queries_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT query_id, email, mobile, query_heading, query_description,
               query_created_time, status, query_closed_time, closing_comment
        FROM client_queries
        WHERE email = %s
        ORDER BY query_created_time DESC
    """, (email, ))

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return pd.DataFrame(data)
