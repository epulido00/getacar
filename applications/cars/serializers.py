from rest_framework import serializers
from .models import Car

from applications.users.serializers import UserSerializer

class CarSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Car
        fields = (
            'id',
            'brand',
            'model',
            'year',
            'type_car',
            'transmission',
            'price',
            'image',
            'user',
        )
