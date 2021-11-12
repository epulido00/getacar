from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    GenericAPIView
)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

from .serializers import (
    CarSerializer,
)

from .models import Car 


from django.db.models import Q

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        SAFE_METHODS = ['GET']
        return request.method in SAFE_METHODS

# Create your views here.
class CarView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated|ReadOnly]
    serializer_class = CarSerializer

    def post(self, request):

        Car.objects.create(
            brand=request.data['brand'],
            model=request.data['model'],
            year=request.data['year'],
            type_car=request.data['type_car'],
            transmission=request.data['transmission'],
            price=request.data['price'],
            image=request.data['image'],
            user=self.request.user
        )
        
        serializer = CarSerializer(Car.objects.latest('id'))
        return Response(serializer.data)

    def get(self, request):
        if self.request.GET:
            query = Q()

            if self.request.GET.get('year'):
                query.add(Q(year=self.request.GET.get('year')), Q.AND)
                
            if self.request.GET.get('brand'):
                query.add(Q(brand=self.request.GET.get('brand')), Q.AND)

            if self.request.GET.get('model'):
                query.add(Q(model=self.request.GET.get('model')), Q.AND)
        
            queryset = Car.objects.filter(query)
            serializer = CarSerializer(queryset, many=True)

            return Response(serializer.data)

        else:
            serializer = CarSerializer(Car.objects.all(), many=True)
            return Response(serializer.data)


class CarViewOptions(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated|ReadOnly]
    serializer_class = CarSerializer

    def delete(self, request, pk):
        try:
            car = Car.objects.get(
                id=pk,
                user=self.request.user
            )
            car.delete()

            return Response({})
        except Car.DoesNotExist:
            return Response({'details':'Ha habido un error con tu consulta el auto no existe o no es del usuario'})

    def get(self, request, pk):
        try:
            car = Car.objects.get(id=pk)
            serializer = CarSerializer(car) 
            return Response(serializer.data)
        except Car.DoesNotExist:
            return Response({'details':'El auto al que tratas de acceder no existe'})

