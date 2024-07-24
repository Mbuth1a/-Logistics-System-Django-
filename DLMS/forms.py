from django import forms
from .models import Driver, Vehicle, CoDriver,Product

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['full_name', 'employee_number', 'license_number', 'phone_number', 'email']


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_regno', 'vehicle_model', 'vehicle_type', 'engine_number', 'capacity']
        widgets = {
            'vehicle_regno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Vehicle Registration Number'}),
            'vehicle_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Vehicle Model'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Vehicle Type'}),
            'engine_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Engine Number'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Capacity'}),
        }
        
        
        
        
class CoDriverForm(forms.ModelForm):
    class Meta:
        model = CoDriver
        fields = ['employee_number', 'co_driver_name', 'phone_number', 'email_address']
        widgets = {
            'employee_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'employeeNumber',
                'required': False,
                'placeholder': 'DCL-123',
                'pattern': 'DCL.*',
                'title': 'Employee number must start with "DCL"',
            }),
            'co_driver_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'coDriver',
                'required': True,
                'placeholder': 'Co-driver Name',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'phoneNumber',
                'required': True,
                'pattern': '\\d{10}',
                'placeholder': 'Phone Number',
                'title': 'Phone number must be exactly 10 digits.',
            }),
            'email_address': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'emailAddress',
                'required': True,
                'pattern': '[a-z0-9._%+-]+@gmail\\.com',
                'placeholder': 'Email Address (@gmail.com)',
                'title': 'Email address must end with "@gmail.com"',
            }),
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['description', 'stock_code', 'product', 'unit_of_measure', 'weight_per_metre']