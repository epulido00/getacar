from django.shortcuts import render
from django.contrib.auth.hashers import check_password

# Third Party
from rest_framework.generics import (
    ListAPIView,
    GenericAPIView,
    RetrieveAPIView
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission


from .models import User
from .serializers import UserLoginSerializer, UserRegisterSerializer, UserSerializer

# Create your views here.
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        SAFE_METHODS = ['GET']
        return request.method in SAFE_METHODS


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
         

class UserDetails(GenericAPIView):

    serializer_class = UserSerializer

    
    def get(self, request, pk):

        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)

        return Response({
            'user': serializer.data
        })


class UserUpdate(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = User.objects.get(
            id = self.request.user.pk
        )
        user = UserSerializer(user)
        return Response(user.data)

    def put(self, request):

        required_data = ['email', 'nombres', 'apellidos', 'genero', 'telefono']
        if all(key in request.data for key in required_data):
            user = User.objects.get(
                id = self.request.user.pk
            )

            user.email = request.data['email']
            user.nombres = request.data['nombres']
            user.apellidos = request.data['apellidos']
            user.genero = request.data['genero']
            user.telefono = request.data['telefono']

            user.save()

            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)
        else:
            return Response({
                'details': 'No has pasado los campos requeridos',
                'datos_requeridos': [
                    'email',
                    'nombres',
                    'apellidos',
                    'genero',
                    'telefono'
                ]
            })
        
