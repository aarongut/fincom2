from django.urls import path

from committee import views

urlpatterns = [
    path('', views.edit, name='edit'),
    path('update/<int:committee>/', views.update, name='update'),
    path('fincom/', views.add_to_fincom, name='add_to_fincom'),
    path('fincom/delete', views.remove_fincom, name='remove_fincom'),
    path('new', views.new_committee, name='new_committee'),
]
