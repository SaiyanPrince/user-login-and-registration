import sqlite3

def get_db_connection():
    conn = sqlite3.connect('users.db')
    return conn