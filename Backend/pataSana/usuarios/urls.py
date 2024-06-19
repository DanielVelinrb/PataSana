from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('usuarios/crear', views.crear_usuario, name='crear_usuario'),
    path('login', views.iniciar_sesion, name='iniciar_sesion'),
    path('change_password', views.cambiar_contrasenia, name='cambiar_contrasenia'),
    path('get_users', views.obtener_usuarios, name='obtener_usuarios'),
    path('get_info_user', views.obtener_info_usuario, name='obtener_info_usuario'),
    path('actualizar_datos', views.actualizar, name='actualizar'),
    path('dashboard_admin', views.ir_index, name='dashboard_admin'),
    path('registro', views.registrar_usuario, name='registrarme'),
    path('restablecer_contra', views.recuperar_contrasenia, name='restablecer_contra')
]