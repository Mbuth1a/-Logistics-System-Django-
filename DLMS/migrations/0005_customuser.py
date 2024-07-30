# Generated by Django 5.0.2 on 2024-07-30 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DLMS', '0004_rename_username_driver_employee_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('staff_no', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('second_name', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('USER', 'User')], max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
