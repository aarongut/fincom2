from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from committee.models import Committee
from items.models import Item

def isAuthorised(request, item):
    return (request.user == item.committee.chair
            or request.user.groups.filter(name='Fincom').exists())

def authError():
    return HttpResponseRedirect('/items')

def myItems(user):
    if (user.groups.filter(name='Fincom').exists()):
        return Item.objects.order_by('-date_filed', 'desc')

    comms = []
    for c in Committee.objects.all():
        if (c.chair == user):
            comms.append(c)

    return Item.objects.filter(Q(created_by=user) | Q(committee__in=comms)) \
            .order_by('-date_filed', 'desc')

def pageItems(request, items, status):
    if status != 'M':
        p = Paginator(items.filter(status=status), 8)
    else:
        p = Paginator(items, 8)
    page = request.GET.get(status)

    try:
        return p.page(page)
    except PageNotAnInteger:
        return p.page(1)
    except EmptyPage:
        return p.page(p.num_pages)

@login_required
def list(request):
    template = loader.get_template('items/list.html')
    items = myItems(request.user)
    mine = Item.objects.filter(created_by=request.user).order_by('-date_filed')


    context = {
        'preapproved': pageItems(request, items, Item.PREAPPROVED),
        'processed': pageItems(request, items, Item.PROCESSED),
        'newitems': pageItems(request, items, Item.NEW),
        'rejected': pageItems(request, items, Item.REJECTED),
        'mine': pageItems(request, mine, 'M'),
        'committees': Committee.objects.order_by('name'),
        'fincom': request.user.groups.filter(name='Fincom').exists(),
    }

    return HttpResponse(template.render(context, request))

@login_required
def details(request, item_id):
    I = Item.objects.get(pk=item_id)
    if (not isAuthorised(request, I)
        and request.user != I.created_by):
        return authError()

    template = loader.get_template('items/details.html')
    
    context = {
        'I': I,
        'approve': isAuthorised(request, I),
    }
    return HttpResponse(template.render(context, request))

def approve(request, item_id):
    I = Item.objects.get(pk=item_id)

    if (not isAuthorised(request, I)):
        return authError()

    I.approved_by.add(request.user)
    if (I.committee.chair == request.user and
        I.status == Item.NEW):
        I.status = Item.PREAPPROVED
        I.mail_fincom()
    elif (request.user.groups.filter(name='Fincom').exists()):
        I.status = Item.PROCESSED
        
    I.save()

    return HttpResponseRedirect('/items')

def reject(request, item_id):
    I = Item.objects.get(pk=item_id)

    if (not isAuthorised(request, I)):
        return authError()

    I.status = Item.REJECTED
    I.save()

    return HttpResponseRedirect('/items')

def delete(request, item_id):
    I = Item.objects.get(pk=item_id)

    if (not isAuthorised(request, I)):
        return authError()

    I.delete()

    return HttpResponseRedirect('/items')

def edit(request, item_id):
    I = Item.objects.get(pk=item_id)

    if (not isAuthorised(request, I)
        and request.user != I.created_by):
        return authError()

    if request.method == 'POST':
        if (request.POST.get('desc', None)):
            I.desc = request.POST['desc']
        if (request.POST.get('event', None)):
            I.event = request.POST['event']
        if (request.POST.get('committee', None)):
            I.committee = Committee.objects.get(name=request.POST['committee'])
        if (request.POST.get('cost', None)):
            I.cost = request.POST['cost']
        if (request.POST.get('date', None)):
            I.date_purchased = Item.parseDate(request.POST['date']),
        if (request.POST.get('details', None)):
            I.details = request.POST['details']

        I.save()

        return HttpResponseRedirect('/items/' + str(item_id))
    else:
        template = loader.get_template('items/edit.html')
        
        context = {
            'I': I,
            'committees': Committee.objects.order_by('name'),
        }
        return HttpResponse(template.render(context, request))

def new_form(request):
    if request.method == 'POST':
        if request.FILES['image'].size > 10 * (1 << 20):
            template = loader.get_template('items/new.html')
            context = {
                'committees': Committee.objects.order_by('name'),
                'error': 'Your image file is too large. Maximum size is 20MB',
            }
            return HttpResponse(template.render(context, request))
        item = Item(
            desc = request.POST['desc'],
            event = request.POST['event'],
            committee = Committee.objects.get(name=request.POST['committee']),
            cost = request.POST['cost'],
            date_purchased = Item.parseDate(request.POST['date']),
            details = request.POST['details'],
            date_filed = timezone.now(),
            created_by = request.user,
            status = Item.NEW,
            image = request.FILES['image'],
        )

        item.save()

        item.mail_com_chair()

        return HttpResponseRedirect('/items')

    else:
        template = loader.get_template('items/new.html')
        context = {
            'committees': Committee.objects.order_by('name'),
        }

        return HttpResponse(template.render(context, request))
