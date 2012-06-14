from kiss.views.core import Response
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
        return Response("<h1>Registration</h1>")
