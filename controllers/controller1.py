from kiss.views.core import Response
from kiss.controllers.core import Controller
from kiss.views.templates import TemplateResponse


class Controller1(Controller):
    def post(self, request):
		return Response("<h1>hello first response!</h1>")
    def get(self, request):
        return TemplateResponse("index.html", {"error":0})
