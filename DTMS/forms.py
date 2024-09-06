from django import forms
from DTMS.models import* 
from DTMS.models import LoadTrip
from django.forms import formset_factory
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['date', 'time', 'description', 'driver', 'co_driver', 'vehicle', 'from_location', 'stops', 'to_location', 'est_distance']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only exclude drivers, co-drivers, and vehicles assigned to 'ongoing' trips
        self.fields['driver'].queryset = Driver.objects.exclude(trip__status='ongoing')
        self.fields['co_driver'].queryset = CoDriver.objects.exclude(trip__status='ongoing')
        self.fields['vehicle'].queryset = Vehicle.objects.exclude(trip__status='ongoing')
        
        
        
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
    
class MaintenanceScheduleForm(forms.ModelForm):
    class Meta:
        model = MaintenanceSchedule
        fields = [
            'service_provider',
            'maintenance_date',
            'inspection_date',
            'insurance_date',
            'speed_governor_date',
            'kenha_permit_date'
        ]
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'inspection_date': forms.DateInput(attrs={'type': 'date'}),
            'insurance_date': forms.DateInput(attrs={'type': 'date'}),
            'speed_governor_date': forms.DateInput(attrs={'type': 'date'}),
            'kenha_permit_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
class LoadTripForm(forms.ModelForm):
    class Meta:
        model = LoadTrip
        fields = '__all__'

ProductFormSet = formset_factory(LoadTripForm, extra=1)


class LoadTripProductForm(forms.ModelForm):
    class Meta:
        model = LoadTripProduct
        fields = ['product', 'quantity', 'total_weight']
        

