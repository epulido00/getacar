from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView
)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CarSerializer,
)

from .models import Car 


from django.db.models import Q

# Create your views here.
class CarApiView(ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):

        if self.request.GET:
            query = Q()

            if self.request.GET.get('year'):
                query.add(Q(year=self.request.GET.get('year')), Q.AND)
                
            if self.request.GET.get('brand'):
                query.add(Q(brand=self.request.GET.get('brand')), Q.AND)

            if self.request.GET.get('model'):
                query.add(Q(model=self.request.GET.get('model')), Q.AND)


            return Car.objects.filter(query)
        else:
            return Car.objects.all()


class CarsUser(ListAPIView):
    serializer_class = CarSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Car.objects.get_cars_by_user(self.request.user)
       
class AddCar(CreateAPIView):
    serializer_class = CarSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.user)
        return Response({"Hola"})

    def get_queryset(self):
        return Car.objects.lastest()
