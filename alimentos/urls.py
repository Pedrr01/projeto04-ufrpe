from django.urls import path
from . import views

urlpatterns = [
    path('', views.plano_list, name='plano_list'),
    path('novo/', views.plano_create, name='plano_create'),
    path('toggle/<int:pk>/', views.plano_toggle, name='plano_toggle'),
    path('estatisticas/', views.plano_estatisticas, name='plano_estatisticas'),
]
