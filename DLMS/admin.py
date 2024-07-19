from django.contrib import admin

# Register your models here.
from .models import Driver, Vehicle, CoDriver, Product, Product

admin.site.register(Driver)
admin.site.register(CoDriver)
admin.site.register(Vehicle)
admin.site.register(Product)

