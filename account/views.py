from account.models import *
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the account index.")

def detail(request, account_id):
    return HttpResponse("You're looking at account %s." % account_id)
