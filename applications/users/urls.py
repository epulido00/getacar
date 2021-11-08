from django.urls import path, re_path, include

# My Apps
from . import views

urlpatterns = [
    path('api/register', views.RegisterUser.as_view()),
    path('api/login', views.LoginUser.as_view()),
]
