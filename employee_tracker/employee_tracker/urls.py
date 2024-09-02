"""employee_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from tracking.views import UserViewSet, EmployeeLocationViewSet

# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'locations', EmployeeLocationViewSet)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
# ]


from django.contrib import admin
from django.urls import path
from tracking.views import getusers, login, user_role, start_tracking, get_locations, get_user_journey, stop_tracking

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users', getusers, name='getusers'),
    path('api/login', login, name='login'),
    path('api/user-role', user_role, name='user_role'),
    path('api/start-tracking', start_tracking, name='start_tracking'),
    path('api/stop-tracking', stop_tracking, name='stop_tracking'),
    path('api/locations', get_locations, name='get_locations'),
    path('api/users/<int:user_id>/journey/', get_user_journey, name='get_user_journey'),
]

