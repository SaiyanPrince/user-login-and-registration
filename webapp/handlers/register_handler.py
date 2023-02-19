import tornado.web
from models import users

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = self.application.db.get_user_by_email(email)
        if user:
            self.write('Email already registered')
        else:
            self.application.db.add_user(username, email, password)
            self.write('Registration successful.')