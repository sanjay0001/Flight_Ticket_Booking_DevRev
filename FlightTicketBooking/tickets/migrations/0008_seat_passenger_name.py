# Generated by Django 4.0.1 on 2023-06-13 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_seat_seat_class_seat_seat_price_seat_seat_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='passenger_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
