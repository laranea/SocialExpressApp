import tornado.ioloop
import tornado.web
from  tornado.template import Loader
from connectdb import ConnectDB


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def session(self):
        return self.application.session

    def get_userid(self):
        connection = ConnectDB()
        sql = "SELECT id FROM user WHERE email=" + self.current_user
        data = connection.connect(sql)
        for user in data:
            user_id = user[0]
            break
        return str(user_id)


