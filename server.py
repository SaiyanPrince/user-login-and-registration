import tornado.ioloop
import tornado.web
import tornado.escape
from handlers.main_handler import MainHandler
from handlers.login_handler import LoginHandler
from handlers.register_handler import RegisterHandler
from models import users

# Define the email server settings
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_FROM = 'example@gmail.com'
EMAIL_PASSWORD = 'password'

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/login', LoginHandler),
            (r'/register', RegisterHandler),
        ]
        settings = {
            'cookie_secret': 'your-cookie-secret',
            'login_url': '/login',
            'template_path': 'templates',
            'static_path': 'static',
            'debug': True
        }
        self.db = users.DB()
        super(Application, self).__init__(handlers, **settings)

if __name__ == '__main__':
    application = Application()
    application.listen(8888)
    print('App is listening on port 8888!!')
    tornado.ioloop.IOLoop.instance().start()