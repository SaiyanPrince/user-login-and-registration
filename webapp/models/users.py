import sqlite3

# Define the database connection and table
class Users:
    def get_user_by_email_and_password(self, db, email, password):
        connection = db.cursor()
        connection.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = connection.fetchone()


        return user

    def get_user_by_email(self, db, email):
        connection = db.cursor()
        connection.execute("SELECT * FROM users WHERE email=?", (email,))
        user = connection.fetchone()

        return user

    def add_user(self, db, username, email, password):
        connection = db.cursor()
        connection.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        self.conn.commit()
