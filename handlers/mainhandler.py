import tornado.ioloop
import tornado.web
from  tornado.template import Loader

#import logging
#logger = logging.getLogger('boilerplate.' + __name__)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")