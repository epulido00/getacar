from django.contrib import admin
from django.urls import path

from . import views

app_name = "cars_app"

urlpatterns = [
    path(
        'api/cars/',
        views.CarView.as_view(),
    ),
    path(
        'api/cars/<pk>/',
        views.CarViewOptions.as_view(),
    ),
]
