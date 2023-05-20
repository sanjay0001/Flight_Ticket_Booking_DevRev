from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields=["name", "email"]
    list_display = ['name','email', 'contactno', 'age']

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    search_fields=["flight_number", "flight_name"]
    list_display = ['flight_number','flight_name']

admin.site.register(Flight_Book)