# Generated by Django 5.0.2 on 2024-07-24 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DTMS', '0005_loadtrip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadtrip',
            name='total_weight',
            field=models.FloatField(),
        ),
    ]
