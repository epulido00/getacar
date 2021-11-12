from django.shortcuts import render
from django.contrib.auth.hashers import check_password

# Third Party
from rest_framework.generics import (
    ListAPIView,
    GenericAPIView
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .models import User
from .serializers import UserLoginSerializer, UserRegisterSerializer
from applications.cars.models import Car
from applications.cars.serializers import CarSerializer

# Create your views here.
class RegisterUser(GenericAPIView):

    serializer_class = UserRegisterSerializer

    def post(self, request):
        try:
            user = User.objects.get(email=request.data['email'])

            return Response({'details':'El correo que ingresaste ya esta dado de alta'})
        except User.DoesNotExist:
            user = User.objects.create_user(
                request.data['email'],
                request.data['password'],
                nombres=request.data['nombres'],
                apellidos=request.data['apellidos'],
                genero=request.data['genero'],
                telefono=request.data['telefono']
            )

            token = Token.objects.create(user=user)

            return Response({
                'token':token.key,
                'users': {
                    'id':user.pk,
                    'email':user.email,
                    'nombres':user.nombres,
                    'apellidos':user.apellidos,
                    'telefono':user.telefono
                }
            })


class LoginUser(GenericAPIView):

    serializer_class = UserLoginSerializer

    def post(self, request):
        try:
            user = User.objects.get(email=request.data['email'])

            pwd_valid = check_password(request.data['password'], user.password)

            if pwd_valid:
                token = Token.objects.get(user=user)
                return Response({
                    'token':token.key,
                    'users': {
                        'id':user.pk,
                        'email':user.email,
                        'nombres':user.nombres,
                        'apellidos':user.apellidos,
                        'telefono':user.telefono
                    }
                })
            else:
                return Response({'details':'La contraseña no es correcta'})

        except User.DoesNotExist:
            return Response({'details':'El correo no existe'})
         
