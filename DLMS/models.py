from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
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
    def create_user(self, staff_no, first_name, second_name, password, role, department, **extra_fields):
        if not staff_no:
            raise ValueError('The Staff No field must be set')
        user = self.model(
            staff_no=staff_no,
            first_name=first_name,
            second_name=second_name,
            department=department,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, staff_no, first_name, second_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(staff_no, first_name, second_name, password, role='ADMIN', **extra_fields)

class CustomUser(AbstractBaseUser):
    staff_no = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    department = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=[('ADMIN', 'Admin'), ('USER', 'User')])
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'staff_no'
    REQUIRED_FIELDS = ['first_name', 'second_name', 'department', 'role']    
    