from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import EmployeeLocation
from .serializers import UserSerializer, EmployeeLocationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'is_admin': user.is_superuser,
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['get'], url_path='user-role')
    def user_role(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'is_admin': user.is_superuser
        })


class EmployeeLocationViewSet(viewsets.ModelViewSet):
    queryset = EmployeeLocation.objects.all()
    serializer_class = EmployeeLocationSerializer

    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['post'], url_path='start-tracking')
    def start_tracking(self, request):
        user = request.user
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        location = EmployeeLocation.objects.create(user=user, latitude=latitude, longitude=longitude)
        return Response(EmployeeLocationSerializer(location).data)

    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['get'], url_path='locations')
    def get_locations(self, request):
        if not request.user.is_admin:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        locations = EmployeeLocation.objects.all()
        return Response(EmployeeLocationSerializer(locations, many=True).data)
