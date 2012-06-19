

import tornado.httpserver
import tornado.ioloop
import tornado.web
#from tornado.options import options

from settings import settings
from urls import url_patterns
#from db import ConnectDB

class TornadoBoilerplate(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)
        #self.session = ConnectDB()


def main():
    app = TornadoBoilerplate()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
