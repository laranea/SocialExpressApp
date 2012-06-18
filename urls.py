from handlers.mainhandler import MainHandler
from handlers.users import *
import tornado
from settings import MEDIA_ROOT as static_path

url_patterns = [
    (r"/", MainHandler),
    (r"/wizard", UserWizardHandler),
    (r"/register", UserRegisterHandler),
]
