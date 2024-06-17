from django.urls import path
from . import views


urlpatterns = [
    path('productos/registrar', views.registrar_producto, name='registrar_producto'),
]