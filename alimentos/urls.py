from django.urls import path
from . import views

urlpatterns = [
    path('', views.plano_list, name='plano_list'),
    path('novo/', views.plano_create, name='plano_create'),
]
