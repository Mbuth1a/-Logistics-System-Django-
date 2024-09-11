from django.db import models
from DLMS.models import*
from django.utils import timezone
from decimal import Decimal

# Create your models here.
class Trip(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('ended', 'Ended'),
    ]
    
    date = models.DateField()
    time = models.TimeField()
    day = models.CharField(max_length=10)
    description = models.CharField(max_length=20, choices=[
        ('Pick-up', 'Pick-up'),
        ('Delivery', 'Delivery'),
        ('Sale Trip', 'Sale Trip'),
    ])
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    co_driver = models.ForeignKey(CoDriver, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=100)
    stops = models.CharField(max_length=200, null=True, blank=True)
    to_location = models.CharField(max_length=100)
    est_distance = models.CharField(max_length=100)
    start_odometer = models.CharField(max_length=100, null= True)
    end_odometer = models.CharField(max_length=100, null=True)
    actual_distance = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing') 
    end_time = models.DateTimeField(null=True, blank=True)
    
    def end_trip(self):
        self.status = 'ended'
        self.end_time = timezone.now()
        self.save()
    
    def __str__(self):
        return f"|{self.vehicle}|   |{self.from_location}|  |{self.stops}|  |{self.to_location}| |{self.driver}|  |{self.co_driver}|"
    
class LoadTrip(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='LoadTripProduct')

    def __str__(self):
        return f"Load for {self.trip}"

class LoadTripProduct(models.Model):
    load_trip = models.ForeignKey(LoadTrip, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_weight = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product} for {self.load_trip}"
    
class Expenses(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    driver_expense = models.DecimalField(max_digits=10, decimal_places=2)
    co_driver_expense = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Trip ID: {self.trip.id}, Driver Expense: {self.driver_expense}, Co-Driver Expense: {self.co_driver_expense}"
    
    
class Fuel(models.Model):
    trip = models.OneToOneField('Trip', on_delete=models.CASCADE)
    fuel_consumed = models.DecimalField(max_digits=10, decimal_places=2)  # Fuel consumed in liters or another unit
    created_at = models.DateTimeField(default=timezone.now)
    date = models.DateField()
    
    def __str__(self):
        return f"Fuel record for Trip ID: {self.trip.id} - {self.fuel_consumed} liters"


# Garage
class Garage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    issue_description = models.TextField()
    checked_in_at = models.DateTimeField(default=timezone.now)
    checked_out_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Garage record for Vehicle ID: {self.vehicle.id}"
    
    
    
class MaintenanceSchedule(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    service_provider = models.CharField(max_length=100)
    maintenance_date = models.DateField()
    inspection_date = models.DateField()
    insurance_date = models.DateField()
    speed_governor_date = models.DateField()
    kenha_permit_date = models.DateField()
    track_solid_date = models.DateField( null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Maintenance Schedule for {self.vehicle.vehicle_regno}"



    
    
class Bike(models.Model):
    name = models.CharField(max_length=100)
    expiry_date = models.DateField()

    def __str__(self):
        return self.name

    def days_remaining(self):
        today = timezone.now().date()
        delta = self.expiry_date - today
        return delta.days