import tornado.web
import tornado.escape
from models import users

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        user = self.application.db.get_user_by_email_and_password(email, password)
        if user:
            self.set_secure_cookie('user', tornado.escape.json_encode(user[0]))
            self.redirect('/')
        else:
            self.write('Invalid login')