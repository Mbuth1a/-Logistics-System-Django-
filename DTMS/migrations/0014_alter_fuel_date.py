# Generated by Django 5.0.2 on 2024-07-27 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DTMS', '0013_fuel_created_at_alter_fuel_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuel',
            name='date',
            field=models.DateField(),
        ),
    ]
