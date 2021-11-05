from django.shortcuts import render
from django.contrib.auth.hashers import check_password

# Third Party
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


from .models import User

# Create your views here.
class RegisterUser(APIView):
    def post(self, request):
        user = User.objects.create_user(
            request.data['email'],
            request.data['password'],
            nombres=request.data['nombres'],
            apellidos=request.data['apellidos'],
        )

        token = Token.objects.create(user=user)

        return Response({
            'token':token.key,
            'users': {
                'id':user.pk,
                'email':user.email,
                'nombres':user.nombres,
                'apellidos':user.apellidos
            }
        })


class LoginUser(APIView):
    def post(self, request):
        try:
            user = User.objects.get(email='edwin@hotmail.com')

            pwd_valid = check_password(request.data['password'], user.password)

            if pwd_valid:
                token = Token.objects.get(user=user)
                return Response({
                    'token':token.key,
                    'users': {
                        'id':user.pk,
                        'email':user.email,
                        'nombres':user.nombres,
                        'apellidos':user.apellidos
                    }
                })
            else:
                return Response({'details':'La contraseña no es correcta'})

        except User.DoesNotExist:
            return Response({'details':'El correo no existe'})
         
