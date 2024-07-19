from django.db import models

class Driver(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"  ({self.username}) {self.first_name} {self.last_name} "
    
    
    
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
    
# Display the vehicle model as the object representation
# class Trip(models.Model):
#     TRIP_TYPES = [
#         ('delivery', 'Delivery'),
#         ('sales', 'Sales Trip'),
#         ('pickup', 'Pick Up'),
#     ]

#     driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     departure_location = models.CharField(max_length=255)
#     departure_time = models.DateTimeField()
#     arrival_destination = models.CharField(max_length=255)
#     arrival_time = models.DateTimeField()
#     trip_type = models.CharField(max_length=50, choices=TRIP_TYPES)

#     def __str__(self):
#         return f"{self.trip_type} - {self.driver} - {self.vehicle}"
#     def __str__(self):
#         return f"{self.trip_type} - {self.driver} - {self.vehicle}"

# class Cargo(models.Model):
#     trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
#     driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
#     description = models.TextField()
#     weight = models.FloatField()
#     handling_requirements = models.TextField()

# class FuelConsumption(models.Model):
#     trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
#     fuel_used = models.FloatField()
#     average_fuel_consumption = models.FloatField()
