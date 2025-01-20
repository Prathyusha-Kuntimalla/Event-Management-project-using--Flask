import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='9490305710@Pra',  # Replace with your MySQL password
        database='event_management'
    )
    return conn
