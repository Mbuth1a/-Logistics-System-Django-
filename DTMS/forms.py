from django import forms
from DTMS.models import*
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'date', 'time', 'day', 'description',  
            'driver', 'co_driver', 'vehicle', 'from_location', 'to_location', 'est_distance'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'day': forms.Select(choices=[
                ('Monday', 'Monday'),
                ('Tuesday', 'Tuesday'),
                ('Wednesday', 'Wednesday'),
                ('Thursday', 'Thursday'),
                ('Friday', 'Friday'),
                ('Saturday', 'Saturday'),
                ('Sunday', 'Sunday'),
            ]),
            'description': forms.Select(choices=[
                ('Pick-up', 'Pick-up'),
                ('Delivery', 'Delivery'),
                ('Sale Trip', 'Sale Trip'),
            ]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'].queryset = Driver.objects.filter(trip__isnull=True)
        self.fields['co_driver'].queryset = CoDriver.objects.filter(trip__isnull=True)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(trip__isnull=True)
        
        
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['trip', 'vehicle_reg_no', 'driver_full_name', 'driver_amount', 'co_driver_name', 'co_driver_amount']
        widgets = {
            'trip': forms.HiddenInput(),  # Hide this field if setting trip ID in view
            'driver_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'co_driver_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'vehicle_reg_no': forms.TextInput(attrs={'class': 'form-control'}),
            'driver_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'co_driver_name': forms.TextInput(attrs={'class': 'form-control'}),
        }