from django import forms
from .models import Driver, Vehicle, CoDriver,Product
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
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
       
class SignUpForm(UserCreationForm):
    staff_no = forms.CharField(max_length=30, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    second_name = forms.CharField(max_length=100, required=True)
    department = forms.CharField(max_length=100, required=True)
    role = forms.ChoiceField(choices=[('ADMIN', 'Admin'), ('USER', 'User')], required=True)

    class Meta:
        model = CustomUser
        fields = ('staff_no', 'first_name', 'second_name', 'department', 'role', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match")
        
        return cleaned_data