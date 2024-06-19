from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('mascotas/registrar', views.registrar_mascota, name='registrar_mascota'),
    path('mascotas/borrar', views.borrar_registro, name='borrar_registro'),
    path('mascotas/listar', views.obtener_mascotas, name='obtener_mascotas'),
    path('mascotas/info/', views.obtener_info_mascota, name='obtener_info_mascota'),
    path('mascotas/actualizar', views.actualizar, name='actualizar')
]