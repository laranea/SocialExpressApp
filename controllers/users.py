from kiss.views.core import Response, RedirectResponse
from kiss.controllers.core import Controller
from kiss.views.templates import TemplateResponse
from models.models import *


class UserLogin(Controller):

    def get(self, request):
        return TemplateResponse("index.html", {'error': 0})

    def post(self, request):
        email = request.values['email']
        password =  request.values['password']
        try:
            User.get(email=email, password=password)
        except:
            return TemplateResponse("index.html", {'error': 1}) 
        return RedirectResponse('/wizard')


class UserProfile(Controller):

    def get(self, request):
        return TemplateResponse("wizard.html", {})

class UserRegistration(Controller):

    def get(self, request):
        return TemplateResponse("register.html", {})

    

class UserRegister(Controller):

    def post(self, request):
        email = request.values['email']
        password =  request.values['password'] 
        company = request.values['company']
        try:
            user = User()
            user.last_login = "2012-06-15 00:00:00"
            user.date_joined = "2012-06-15 00:00:00"
            user.email = email
            user.password = password
            user.save()
        except:
            return RedirectResponse('/registration') 
        return RedirectResponse('/wizard') 

