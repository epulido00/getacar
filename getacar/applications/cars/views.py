from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.generics import (
    ListAPIView,
)

from .serializers import (
    CarSerializer,
)

from .models import Car 

# Create your views here.
class CarApiView(ListAPIView):

    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.all()
        
