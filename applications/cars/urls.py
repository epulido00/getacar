from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('api/cars', views.CarApiView.as_view()),
    path('api/cars-by-user', views.CarsUser.as_view()),
    path('api/cars/add', views.AddCar.as_view()),
]
