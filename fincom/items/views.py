from django.shortcuts import HttpResponse
from django.template import loader
from models import Item
from committee.models import Committee


# Create your views here.
def list(request):
    template = loader.get_template('items/list.html')
    context = {
        'items': Item.objects.all(),
    }

    return HttpResponse(template.render(context, request))

def new_form(request):
    template = loader.get_template('items/new.html')
    context = {
        'committees': Committee.objects.order_by('name'),
    }

    return HttpResponse(template.render(context, request))
