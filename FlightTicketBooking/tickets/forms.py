from django import forms
from .models import *
from django.forms import DateTimeInput,TextInput,NumberInput

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        model._meta.get_field('takeoff_date').verbose_name = "Departure Date"
        model._meta.get_field('takeoff_time').verbose_name = "Departure Time"
        fields = '__all__'
        widgets = {
            'takeoff_time': DateTimeInput(attrs={'type': 'time','class':"form-control form-control-lg"}),
            'arrival_time': DateTimeInput(attrs={'type': 'time','class':"form-control form-control-lg"}),
            'takeoff_date': DateTimeInput(attrs={'type': 'date','class':"form-control form-control-lg"}),
            'arrival_date': DateTimeInput(attrs={'type': 'date','class':"form-control form-control-lg"}),
            'flight_number': TextInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'flight_name': TextInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'flight_from': TextInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'flight_to': TextInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'flight_duration': NumberInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'number_of_seats': NumberInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'seats_booked': NumberInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'price': NumberInput(attrs={'type':'text','class': "form-control form-control-lg"}),

        }