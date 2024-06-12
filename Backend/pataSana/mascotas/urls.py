from django.urls import path
from . import views


urlpatterns = [
    path('mascotas/registrar', views.registrar_mascota, name='registrar_mascota'),
]