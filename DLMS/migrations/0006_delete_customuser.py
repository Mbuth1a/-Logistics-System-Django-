# Generated by Django 5.0.2 on 2024-07-31 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DLMS', '0005_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]