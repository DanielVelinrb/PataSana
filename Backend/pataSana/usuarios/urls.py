from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('usuarios/crear', views.crear_usuario, name='crear_usuario'),
]