import tornado.ioloop
import tornado.web
from  tornado.template import Loader


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def session(self):
        return self.application.session


