import tornado.ioloop
import tornado.web
from  tornado.template import Loader
from basehandler import BaseHandler
from connectdb import ConnectDB

#import logging
#logger = logging.getLogger('boilerplate.' + __name__)


class UserRegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html")

    def post(self):
        connection = ConnectDB()
        email = self.get_argument("email")
        password = self.get_argument("password")
        company = self.get_argument("company")
        sql = "INSERT INTO user (email, password, last_login, date_joined) VALUES ('%s', '%s', '2012-06-12 00:00:00', '2012-06-12 00:00:00')" % (email, password)
        print sql
        data = connection.connect(sql, 1)
        self.redirect('/wizard')


class UserWizardHandler(BaseHandler):


    @tornado.web.authenticated
    def get(self):
        self.render("wizard.html")


