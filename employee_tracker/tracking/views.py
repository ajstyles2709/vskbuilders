# from django.shortcuts import render

# # Create your views here.
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from django.contrib.auth.models import User
# from .models import EmployeeLocation
# from .serializers import UserSerializer, EmployeeLocationSerializer
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.views.decorators.csrf import csrf_exempt


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     @csrf_exempt
#     @action(detail=False, methods=['post'], url_path='login')
#     def login(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user_id': user.id,
#                 'is_admin': user.is_superuser,
#             })
#         else:
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#     @csrf_exempt
#     @action(detail=False, methods=['get'], url_path='user-role')
#     def user_role(self, request):
#         user = request.user
#         return Response({
#             'username': user.username,
#             'is_admin': user.is_superuser
#         })


# class EmployeeLocationViewSet(viewsets.ModelViewSet):
#     queryset = EmployeeLocation.objects.all()
#     serializer_class = EmployeeLocationSerializer

#     @csrf_exempt
#     @action(detail=False, methods=['post'], url_path='start-tracking')
#     def start_tracking(self, request):
#         user = request.user
#         latitude = request.data.get('latitude')
#         longitude = request.data.get('longitude')
#         location = EmployeeLocation.objects.create(user=user, latitude=latitude, longitude=longitude)
#         return Response(EmployeeLocationSerializer(location).data)

#     @       csrf_exempt
#     @action(detail=False, methods=['get'], url_path='locations')
#     def get_locations(self, request):
#         if not request.user.is_admin:
#             return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
#         locations = EmployeeLocation.objects.all()
#         return Response(EmployeeLocationSerializer(locations, many=True).data)



from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .models import EmployeeLocation
from .serializers import UserSerializer, EmployeeLocationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def login(request):
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

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_role(request):
    user = request.user
    return Response({
        'username': user.username,
        'is_admin': user.is_superuser
    })

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_tracking(request):
    user = request.user
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    location = EmployeeLocation.objects.create(user=user, latitude=latitude, longitude=longitude)
    return Response(EmployeeLocationSerializer(location).data)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_locations(request):
    if not request.user.is_superuser:
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
    locations = EmployeeLocation.objects.all()
    return Response(EmployeeLocationSerializer(locations, many=True).data)
