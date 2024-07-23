from django.db import models
from DLMS.models import*
from decimal import Decimal
# Create your models here.
class Trip(models.Model):
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
    to_location = models.CharField(max_length=100)
    est_distance = models.CharField(max_length=100)
    
    
    def __str__(self):
        return f"|{self.vehicle}|   |{self.from_location}|  |{self.driver}|  |{self.co_driver}|"
    
    
class LoadTrip(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Assuming quantity is positive
    type = models.CharField(max_length=10, choices=[('pieces', 'Pieces'), ('rolls', 'Rolls')])
    total_weight = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        # Calculate total weight before saving
        if self.product:
            # Convert weight_per_metre to float
            weight_per_metre = float(self.product.weight_per_metre)
            if self.type == 'pieces':
                self.total_weight = Decimal(self.quantity * weight_per_metre)
            elif self.type == 'rolls':
                # Assuming rolls are handled similarly
                self.total_weight = Decimal(self.quantity * weight_per_metre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"LoadTrip {self.id} - Trip {self.trip.id} - Product {self.product.stock_code}"