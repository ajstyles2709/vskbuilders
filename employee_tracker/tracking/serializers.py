from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EmployeeLocation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EmployeeLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLocation
        fields = '__all__'
