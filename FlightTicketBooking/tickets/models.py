from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    contactno = models.CharField(max_length=20)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=32)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
      return self.name
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Flight(models.Model):
    flight_number=models.CharField(max_length=100,unique=True)
    flight_name = models.CharField(max_length=100)
    flight_from = models.CharField(max_length=100)
    flight_to = models.CharField(max_length=100)
    takeoff_date = models.DateField()
    arrival_date = models.DateField()
    takeoff_time = models.TimeField()
    arrival_time = models.TimeField()
    flight_duration = models.FloatField()
    number_of_seats = models.IntegerField()
    price = models.IntegerField()
    seats_booked = models.IntegerField()

    def __str__(self):
      return self.flight_number
    
class Flight_Book(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

   def __str__(self):
      return f"{str(self.flight)}, {str(self.user)}"
   