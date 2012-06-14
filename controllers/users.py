from kiss.views.core import Response
from kiss.controllers.core import Controller
from kiss.views.templates import TemplateResponse


class UserRegister(Controller):

    def post(self, request):
        print "------user reg---"
        print request.params['email']
        return Response("<h1>Registration</h1>")
