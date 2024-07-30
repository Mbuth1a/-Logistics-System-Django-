from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import*


class Driver(models.Model):
    full_name = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"  ({self.employee_number}) {self.full_name}  "
    
    
    
class CoDriver(models.Model):
    employee_number = models.CharField(max_length=50, unique=True)
    co_driver_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email_address = models.EmailField()

    def __str__(self):
        return f"({self.employee_number}) {self.co_driver_name}"
class Vehicle(models.Model):
    vehicle_regno = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    engine_number = models.CharField(max_length=100)
    capacity = models.CharField(max_length=100)

    def __str__(self):
        return f"({self.vehicle_regno} ){self.vehicle_model} {self.vehicle_type}"
    
class Product(models.Model):
    description = models.CharField(max_length=255)
    stock_code = models.CharField(max_length=50)
    product = models.CharField(max_length=100)
    unit_of_measure = models.CharField(max_length=50)
    weight_per_metre = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"({self.stock_code}) ({self.product})  ({self.description})  ({self.unit_of_measure})  ({self.weight_per_metre})"
    


#  SIGNUP AND LOGIN MODELS




class CustomUserManager(BaseUserManager):
    def create_user(self, staff_no, first_name, second_name, password, department, role, **extra_fields):
        if not staff_no:
            raise ValueError('The Staff No must be set')
        if not password:
            raise ValueError('The Password must be set')

        user = self.model(
            staff_no=staff_no,
            first_name=first_name,
            second_name=second_name,
            department=department,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.is_superuser = (role == 'ADMIN')
        user.is_staff = (role == 'ADMIN')
        user.save(using=self._db)
        return user

    def create_superuser(self, staff_no, first_name, second_name, password, department, **extra_fields):
        extra_fields.setdefault('role', 'ADMIN')
        return self.create_user(staff_no, first_name, second_name, password, department, **extra_fields)

class CustomUser(AbstractBaseUser):
    staff_no = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=[('ADMIN', 'Admin'), ('USER', 'User')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'staff_no'
    REQUIRED_FIELDS = ['first_name', 'second_name', 'department']

    def __str__(self):
        return self.staff_no

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_full_name(self):
        return f"{self.first_name} {self.second_name}"

    def get_short_name(self):
        return self.first_name