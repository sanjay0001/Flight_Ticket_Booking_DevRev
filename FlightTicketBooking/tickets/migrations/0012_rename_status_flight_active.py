# Generated by Django 4.0.1 on 2023-06-14 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0011_delete_flight_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='status',
            new_name='active',
        ),
    ]
