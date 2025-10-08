from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # <-- IMPORTAÇÃO QUE FALTAVA
import core.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('usuarios/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('dashboard/', core.views.dashboard, name='dashboard'),
]