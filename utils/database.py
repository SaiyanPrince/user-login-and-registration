import mysql.connector

def get_db_connection():
    conn = mysql.connect('users.db')
    return conn