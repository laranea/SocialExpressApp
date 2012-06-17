import tornado.ioloop
import tornado.web
from  tornado.template import Loader

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
	loader = tornado.template.Loader("/home/ubuntu/socialexpress/views/templates")
	self.write(loader.load("index.html").generate(error="hello"))

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
