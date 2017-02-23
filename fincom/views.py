from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.template import loader

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/items')

    template = loader.get_template('fincom/index.html')
    return HttpResponse(template.render({}, request))

def encrypt(request):
    return HttpResponse('EJpPgYRpZkFhuxZEpocd9j0Xy58rA1swzbItXAgXV2M.g4Ct3egntTJZl1LOzJH8v9Ri24BQ7blYjcbzPucJVE4', request)

def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')
