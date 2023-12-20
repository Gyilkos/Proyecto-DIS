# myapp/urls.py
from django.urls import path
from .views import arrendar_camioneta, entregar_camioneta, mantenimiento_camioneta, ver_estados

urlpatterns = [
    path('arrendar/', arrendar_camioneta, name='arrendar_camioneta'),
    path('entregar/', entregar_camioneta, name='entregar_camioneta'),
    path('mantenimiento/', mantenimiento_camioneta, name='mantenimiento_camioneta'),
    path('estados/', ver_estados, name='ver_estados'),
]
