from django.shortcuts import HttpResponse
from django.template import loader
from models import Item


# Create your views here.
def list(request):
    template = loader.get_template('items/list.html')
    context = {
        'items': Item.objects.all(),
    }

    return HttpResponse(template.render(context, request))
