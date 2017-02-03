from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^new$', views.new_form, name='new_form'),
]
