
CLIENT QUERY MANAGEMENT SYSTEM


------------------------------------------------------------

Project Description


The Client Query Management System is a simple web-based application built using
Python, MySQL, and Streamlit. It allows clients to submit their queries and enables
support teams to track, manage, and close those queries efficiently.

This project is designed for beginners to understand how real-world applications
use databases, dashboards, and user roles.


------------------------------------------------------------

Tech stack

Language      : Python
Database      : MySQL
Frontend      : Streamlit
Libraries     : pandas, datetime, mysql-connector-python


-------------------------------------------------------------

Features

Login and Register Screen
    1. User has to register for the first time both client and support
    2. Post registeration user can login.
    3. Based on the login role user will be navigated to the respective screen.
    4. Validation are added for registeration and login


Client Login & Query Submission
    1. Clients can log in and submit queries
    2. Each query includes email, mobile number, heading, and description
    3. Queries are marked as "Open" by default
    4. Client can view their queries 

 Support Team Dashboard
   View all client queries
   Filter queries by status (Open / Closed) and catgeories
   Close queries with comments
   Automatically records query closed time
   Support team can view the Service Efficiency, Support Load Monitoring, Backlog - Open Queries.


-----------------------------------------------------------------------------

Installation and execution Steps

Install Python (version 3.8 or above)
Install required libraries:
pip install streamlit pandas mysql-connector-python as requirement.txt
Create a MySQL database and required tables
Update database credentials in the Python code
Run the Streamlit app.py


-------------------------------------------------------------------------------







