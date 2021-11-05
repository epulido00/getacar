from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('cars', views.CarApiView.as_view()),
]
