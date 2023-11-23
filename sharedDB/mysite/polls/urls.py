from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chao", views.chao, name="chao"),
]