import tornado.web

from models import Users
from utils.database import get_db_connection

class RegisterHandler(tornado.web.RequestHandler):
    def __init__(self):
        self.db = get_db_connection()

    def get(self):
        self.render('register.html')

    def post(self):
        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = Users.get_user_by_email(self.db, email)
        if user:
            self.write('Email already registered')
        else:
            Users.add_user(self.db, username, email, password)
            self.write('Registration successful.')
