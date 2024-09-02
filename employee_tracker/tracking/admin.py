from django.contrib import admin

# Register your models here.
from .models import EmployeeLocation

@admin.register(EmployeeLocation)
class EmployeeLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude', 'timestamp')
    search_fields = ('user__username',)
    list_filter = ('timestamp',)