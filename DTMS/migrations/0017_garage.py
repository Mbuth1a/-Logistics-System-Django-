# Generated by Django 5.0.2 on 2024-08-01 08:26

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DLMS', '0006_delete_customuser'),
        ('DTMS', '0016_delete_stop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Garage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_description', models.TextField()),
                ('checked_in_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('checked_out_at', models.DateTimeField(blank=True, null=True)),
                ('vehicle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='DLMS.vehicle')),
            ],
        ),
    ]
