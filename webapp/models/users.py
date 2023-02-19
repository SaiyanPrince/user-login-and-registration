import sqlite3

# Define the database connection and table
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT,
                           email TEXT,
                           password TEXT)''')
        self.conn.commit()

    def get_user_by_email_and_password(self, email, password):
        self.c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = self.c.fetchone()
        return user

    def get_user_by_email(self, email):
        self.c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = self.c.fetchone()
        return user

    def add_user(self, username, email, password):
        self.c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        self.conn.commit()