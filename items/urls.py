from django.conf.urls import url
from items import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^(?P<item_id>\d+)/$', views.details, name='details'),
    url(r'^(?P<item_id>\d+)/approve$', views.approve, name='approve'),
    url(r'^(?P<item_id>\d+)/reject$', views.reject, name='reject'),
    url(r'^(?P<item_id>\d+)/edit$', views.edit, name='edit'),
    url(r'^(?P<item_id>\d+)/delete$', views.delete, name='delete'),
    url(r'^new$', views.new_form, name='new_form'),
]
