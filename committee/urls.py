from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.edit, name='edit'),
    url(r'^update/(?P<committee>\d+)/$', views.update, name='update'),
    url(r'^fincom/$', views.add_to_fincom, name='add_to_fincom'),
    url(r'^fincom/delete$', views.remove_fincom, name='remove_fincom'),
    url(r'^new$', views.new_committee, name='new_committee'),
]
