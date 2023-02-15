import tornado.ioloop
import tornado.web
import tornado.escape
import sqlite3
import smtplib
from email.mime.text import MIMEText

# Define the database connection and table
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT,
              email TEXT,
              password TEXT)''')
conn.commit()

# Define the email server settings
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_FROM = 'example@gmail.com'
EMAIL_PASSWORD = 'password'

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to my Webapp")

# Define the login handler
class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        if user:
            self.set_secure_cookie('user', tornado.escape.json_encode(user[0]))
            self.redirect('/')
        else:
            self.write('Invalid login')

# Define the registration handler
class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()
        if user:
            self.write('Email already registered')
        else:
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            self.send_verification_email(email)
            self.write('Registration successful. Please check your email for verification.')

    def send_verification_email(self, email):
        verification_link = 'http://example.com/verify?email=' + email
        msg = MIMEText('Please click the following link to verify your email: ' + verification_link)
        msg['Subject'] = 'Email Verification'
        msg['From'] = EMAIL_FROM
        msg['To'] = email
        server = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, [email], msg.as_string())
        server.quit()

# Define the verification handler
class VerifyHandler(tornado.web.RequestHandler):
    def get(self):
        email = self.get_argument('email')
        c.execute("UPDATE users SET verified=1 WHERE email=?", (email,))
        conn.commit()
        self.write('Email verification successful')

# Define the application settings and routes
settings = {
    'cookie_secret': 'your-cookie-secret',
    'login_url': '/login',
    'template_path': 'templates',
    'static_path': 'static',
    'debug': True
}

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/login', LoginHandler),
    (r'/register', RegisterHandler),
    (r'/verify', VerifyHandler),
], **settings)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()