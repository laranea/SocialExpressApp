from account.models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login

def index(request):
    return render_to_response('account/login.html',
                        {})

def detail(request, account_id):
    return HttpResponse("You're looking at account %s." % account_id)

def login(request):
    def errorHandle(error):
        return render_to_response('login.html', {
                'error' : error,
        })
    if request.method == 'POST': # If the form has been submitted...
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # Redirect to a success page.
                    login(request, user)
                    return render_to_response('wizard/index.html', {
                        'username': username,
                    })
                else:
                    # Return a 'disabled account' error message
                    error = u'account disabled'
                    return errorHandle(error)
            else:
                 # Return an 'invalid login' error message.
                error = u'invalid login'
                return errorHandle(error)
    else:
        return render_to_response('login.html', { error: error })