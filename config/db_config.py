# This file contains the MySQL connection settings.
# A function is created so we can reuse the connection everywhere.

import mysql.connector

def get_connection():
    # Connect to your MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",          # your MySQL username
        password="Ch@ru2000",  # your MySQL password
        database="client_query_system"  # database name
    )
    return connection
