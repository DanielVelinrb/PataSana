from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('usuarios/crear', views.crear_usuario, name='crear_usuario'),
    path('login', views.iniciar_sesion, name='iniciar_sesion'),
    path('change_password', views.cambiar_contrasenia, name='cambiar_contrasenia'),
]