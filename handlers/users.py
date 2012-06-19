import tornado.ioloop
import tornado.web
from  tornado.template import Loader
from basehandler import BaseHandler
from connectdb import ConnectDB

#import logging
#logger = logging.getLogger('boilerplate.' + __name__)


class UserRegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html", error=0)

    def post(self):
        connection = ConnectDB()
        email = self.get_argument("email")
        password = self.get_argument("password")
        company = self.get_argument("company")
        sql = "SELECT * FROM user WHERE email='" + email + "'"
        data = connection.connect(sql)
        if data:
            self.render("register.html", error=1)
        sql = "INSERT INTO user (email, password, last_login, date_joined) VALUES ('%s', '%s', '2012-06-12 00:00:00', '2012-06-12 00:00:00')" % (email, password)
        data = connection.connect(sql, 1)
        self.set_secure_cookie("user", tornado.escape.json_encode(email))
        self.redirect('/newweeklyreport')


class UserWizardHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("newweeklyreport.html")


class UserSignout(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.clear_cookie('user')
        self.redirect("/")

