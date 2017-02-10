from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from models import Committee

@login_required
def edit(request):
    if (not request.user.groups.filter(name='Fincom').exists()):
        return HttpResponseRedirect('/items')

    template = loader.get_template('committee/edit.html')

    context = {
        'committees': Committee.objects.order_by('name'),
        'fincom': User.objects.filter(groups__name='Fincom'),
        'users': User.objects.order_by('first_name', 'last_name'),
    }

    return HttpResponse(template.render(context, request))

@login_required
def update(request, committee):
    if (not request.user.groups.filter(name='Fincom').exists()):
        return HttpResponseRedirect('/items')

    committee = Committee.objects.get(pk=committee)

    committee.name = request.POST['name']
    committee.chair = User.objects.get(pk=request.POST['chair'])

    committee.save()

    return HttpResponseRedirect('/committees')
@login_required
def new_committee(request):
    if (not request.user.groups.filter(name='Fincom').exists()):
        return HttpResponseRedirect('/items')

    committee = Committee(
        name = request.POST['name'],
        chair = User.objects.get(pk=request.POST['chair']),
    )

    committee.save()

    return HttpResponseRedirect('/committees')

@login_required
def add_to_fincom(request):
    if (not request.user.groups.filter(name='Fincom').exists()):
        return HttpResponseRedirect('/items')

    user = User.objects.get(pk=request.POST['user'])
    user.groups.add(Group.objects.filter(name='Fincom')[0])

    user.save()

    return HttpResponseRedirect('/committees')

@login_required
def remove_fincom(request):
    if (not request.user.groups.filter(name='Fincom').exists()):
        return HttpResponseRedirect('/items')

    for u in request.POST.getlist('user'):
        user = User.objects.get(pk=u)
        user.groups.remove(Group.objects.filter(name='Fincom')[0])
        user.save()

    return HttpResponseRedirect('/committees')