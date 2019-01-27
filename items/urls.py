from django.urls import path
from items import views

urlpatterns = [
    path(r'', views.list, name='list'),
    path('<int:item_id>/', views.details, name='details'),
    path('<int:item_id>/approve', views.approve, name='approve'),
    path('<int:item_id>/reject', views.reject, name='reject'),
    path('<int:item_id>/edit', views.edit, name='edit'),
    path('<int:item_id>/delete', views.delete, name='delete'),
    path('new', views.new_form, name='new_form'),
]
