from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserRegisterSerializer(serializers.Serializer):
    nombres = serializers.CharField(max_length = 30, required=True) 
    apellidos = serializers.CharField(max_length = 30, required=True)
    genero = serializers.CharField(max_length=1)
    telefono = serializers.CharField(max_length=10, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=20, required=True)
