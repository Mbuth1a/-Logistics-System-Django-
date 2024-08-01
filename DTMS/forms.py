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
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'day': forms.Select(choices=[
                ('Monday', 'Monday'),
                ('Tuesday', 'Tuesday'),
                ('Wednesday', 'Wednesday'),
                ('Thursday', 'Thursday'),
                ('Friday', 'Friday'),
                ('Saturday', 'Saturday'),
                ('Sunday', 'Sunday'),
            ], attrs={'class': 'form-control'}),
            'description': forms.Select(choices=[
                ('Pick-up', 'Pick-up'),
                ('Delivery', 'Delivery'),
                ('Sale Trip', 'Sale Trip'),
            ], attrs={'class': 'form-control'}),
            'from_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter start location'}),
            'to_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter destination'}),
            'est_distance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter estimated distance'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'].queryset = Driver.objects.filter(trip__isnull=True)
        self.fields['co_driver'].queryset = CoDriver.objects.filter(trip__isnull=True)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(trip__isnull=True)
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['driver_expense', 'co_driver_expense']
        

# Garage forms
class GarageForm(forms.ModelForm):
    class Meta:
        model = Garage
        fields = ['vehicle', 'issue_description']

class VehicleSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)