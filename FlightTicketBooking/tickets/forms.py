from django import forms
from .models import *
from django.forms import DateTimeInput,TextInput,NumberInput

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        model._meta.get_field('takeoff_date').verbose_name = "Departure Date"
        model._meta.get_field('takeoff_time').verbose_name = "Departure Time"
        model._meta.get_field('price_business').verbose_name = "Fare of business class (Rs.)"
        model._meta.get_field('price_economy').verbose_name = "Fare of economy class (Rs.)"
        fields = ('flight_name','flight_number','flight_from','flight_to','takeoff_date','takeoff_time','arrival_date','arrival_time', 'price_business','price_economy')
        widgets = {
            'takeoff_time': DateTimeInput(attrs={'type': 'time','class':"form-control form-control-lg"}),
            'arrival_time': DateTimeInput(attrs={'type': 'time','class':"form-control form-control-lg"}),
            'takeoff_date': DateTimeInput(attrs={'type': 'date','class':"form-control form-control-lg"}),
            'arrival_date': DateTimeInput(attrs={'type': 'date','class':"form-control form-control-lg"}),
            'flight_number': TextInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'flight_name': TextInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'flight_from': TextInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'flight_to': TextInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'price_business': NumberInput(attrs={'type':'text','class': "form-control form-control-lg"}),
            'price_economy': NumberInput(attrs={'type':'text','class': "form-control form-control-lg"}),
        }