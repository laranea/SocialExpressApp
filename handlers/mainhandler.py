import tornado.ioloop
import tornado.web
from  tornado.template import Loader
from models.models import *
from connectdb import ConnectDB
from basehandler import BaseHandler

#import logging
#logger = logging.getLogger('boilerplate.' + __name__)

class MainHandler(BaseHandler):

    @property
    def session(self):
        return self.application.session

    def get(self):
        user_id = self.get_secure_cookie("user")
        if user_id:
            self.redirect('/wizard')
        error = 0
        self.render("index.html", error=error)

    def post(self):
        email = self.get_argument("email", default="")
        password = self.get_argument("password", default="")
        connection = ConnectDB()
        sql = "Select * FROM user WHERE email='" + email + "'" + " AND password = '" + password + "'"
        data = connection.connect(sql)
        for user in data:
            self.set_secure_cookie("user", tornado.escape.json_encode(email))
            self.redirect('/wizard')
        else:
            error = 1
            self.render("index.html", error=error)
