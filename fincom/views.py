from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.template import loader

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/items')

    template = loader.get_template('fincom/index.html')
    return HttpResponse(template.render({}, request))

def encrypt(request):
    return HttpResponse('tVQ35BIrm7ybiASBxRMHG2CAO44x-I2BVMqcrv_yJ2k.g4Ct3egntTJZl1LOzJH8v9Ri24BQ7blYjcbzPucJVE4', request)

def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')
