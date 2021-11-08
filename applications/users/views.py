from django.shortcuts import render
from django.contrib.auth.hashers import check_password

# Third Party
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .models import User
from applications.cars.models import Car
from applications.cars.serializers import CarSerializer

# Create your views here.
class RegisterUser(APIView):
    def post(self, request):
        user = User.objects.create_user(
            request.data['email'],
            request.data['password'],
            nombres=request.data['nombres'],
            apellidos=request.data['apellidos'],
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


class LoginUser(APIView):
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
         