from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse, HttpResponse
from DTMS.forms import*
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import datetime
from datetime import timedelta
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET,require_POST

# Create your views here.
def dtms_dashboard(request):
    return render(request, 'dtms_dashboard.html')



def create_trip(request):
    drivers = Driver.objects.all()
    co_drivers = CoDriver.objects.all()
    vehicles = Vehicle.objects.all()

    # Retrieve the choices for the 'description' field from the Trip model
    description_choices = Trip._meta.get_field('description').choices

    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.day = request.POST.get('day')  # Set the day field
            trip.save()
            return redirect('load_trip')  # Replace 'load_trip' with your URL name or path
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    form = TripForm()
    return render(request, 'create_trip.html', {
        'drivers': drivers,
        'co_drivers': co_drivers,
        'vehicles': vehicles,
        'description_choices': description_choices,  # Pass the choices to the template
        'form': form
    })
def search_drivers(request):
    query = request.GET.get('query', '')
    drivers = Driver.objects.filter(name__icontains=query).values('id', 'name')
    return JsonResponse({'drivers': list(drivers)})
# Load Trip Views 

@csrf_protect
def load_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    
    if request.method == 'POST':
        formset = ProductFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                trip_product = form.save(commit=False)
                trip_product.trip = trip
                trip_product.save()
            return redirect('success_url')  # redirect to a success page or another view
    else:
        formset = ProductFormSet()
        
    trip = Trip.objects.all()
    products = Product.objects.all()

    return render(request, 'load_trip.html', {'formset': formset, 'trip': trip})

    
   


def get_trips(request):
    trips = Trip.objects.all()
    data = [
        {
            'id': trip.id,
            'date': trip.date.isoformat(),
            'time': trip.time.isoformat(),
            'day': trip.day,
            'description': trip.description,
            'driver': trip.driver.full_name,  # Assuming Driver model has a 'name' field# Assuming Driver model has a 'name' field
            'co_driver': trip.co_driver.co_driver_name,  # Assuming CoDriver model has a 'name' field
            'vehicle': str(trip.vehicle),  # Using the __str__ representation of Vehicle
            'from_location': trip.from_location,
            'stops': trip.stops,
            'to_location': trip.to_location,
            'est_distance': trip.est_distance
        } for trip in trips
    ]
    return JsonResponse(data, safe=False)

# Expenses
def expenses(request):
    return render(request, 'expenses.html')

def fetch_trips(request):
    trips = Trip.objects.all().values(
        'id', 'vehicle__vehicle_regno', 'date', 'from_location', 'stops', 'to_location', 
        'driver__name', 'co_driver__name'
    )
    return JsonResponse({'trips': list(trips)})

def get_trip_details(request, trip_id):
    try:
        trip = Trip.objects.get(id=trip_id)
        trip_data = {
            'id': trip.id,
            'date': trip.date.isoformat(),
            'time': trip.time.isoformat(),
            'day': trip.day,
            'description': trip.description,
            'driver': trip.driver.full_name,
            'co_driver': trip.co_driver.co_driver_name,
            'vehicle': trip.vehicle.vehicle_regno,
            'from_location': trip.from_location,
            'stops': trip.stops,
            'to_location': trip.to_location,
            'est_distance': trip.est_distance,
        }
        return JsonResponse(trip_data)
    except Trip.DoesNotExist:
        return JsonResponse({'error': 'Trip not found'}, status=404)
@csrf_exempt
def assign_expenses(request):
    if request.method == 'POST':
        trip_id = request.POST.get('tripId')
        driver_expense = request.POST.get('driverExpense')
        co_driver_expense = request.POST.get('coDriverExpense')

        trip = get_object_or_404(Trip, id=trip_id)

        expense = Expenses.objects.create(
            trip=trip,
            driver_expense=driver_expense,
            co_driver_expense=co_driver_expense
        )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)

def fetch_assigned_expenses(request):
    expenses = Expenses.objects.all().values()  # Query to get all expenses
    expenses_list = list(expenses)  # Convert queryset to a list
    return JsonResponse({'expenses': expenses_list})


def fuel(request):
    trips = Trip.objects.filter(fuel__isnull=True)  # Filter trips with no fuel record
    return render(request, 'fuel_records.html', {'trips': trips})
# Saving of the fuel records to the database
@csrf_exempt
def save_fuel(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        fuel_consumed = request.POST.get('fuel_consumed')
        
        try:
            trip = Trip.objects.get(id=trip_id)
            Fuel.objects.create(
                trip=trip,
                fuel_consumed=fuel_consumed,
                date=trip.date
            )
            return JsonResponse({'success': True})
        except Trip.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Trip not found'})

def fetch_fuel_records(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    vehicle_id = request.GET.get('vehicle')
    
    trips = Trip.objects.all()

    if start_date:
        trips = trips.filter(date__gte=parse_date(start_date))
    if end_date:
        trips = trips.filter(date__lte=parse_date(end_date))
    if vehicle_id:
        trips = trips.filter(vehicle_id=vehicle_id)
    
    trip_data = []
    for trip in trips:
        fuel_record = Fuel.objects.filter(trip=trip).first()
        trip_data.append({
            'id': trip.id,
            'vehicle': str(trip.vehicle),
            'date': trip.date.strftime('%Y-%m-%d'),
            'from_location': trip.from_location,
            'to_location': trip.to_location,
            'fuel_consumed': fuel_record.fuel_consumed if fuel_record else None
        })
    
    return JsonResponse({'trips': trip_data})
# Overall reports of monthly consumption per vehicle
def fetch_monthly_consumption(request):
    vehicle_regno = request.GET.get('vehicle')  # Get the vehicle registration number from the request
    monthly_data = {}
    
    # Filter the fuel records by the vehicle registration number
    fuel_records = Fuel.objects.filter(trip__vehicle__vehicle_regno=vehicle_regno)
    
    for record in fuel_records:
        month = record.date.strftime('%Y-%m')
        if month in monthly_data:
            monthly_data[month] += record.fuel_consumed
        else:
            monthly_data[month] = record.fuel_consumed
    
    return JsonResponse({'monthly_data': monthly_data})

def fetch_vehicle_list(request):
    vehicles = Vehicle.objects.all().values('id', 'vehicle_regno')
    return JsonResponse({'vehicles': list(vehicles)})


def fetch_trips(request):
    # Get trips that don't have associated fuel records
    trips_without_fuel = Trip.objects.filter(fuel__isnull=True)

    trips_data = []
    for trip in trips_without_fuel:
        trips_data.append({
            'id': trip.id,
            'vehicle': str(trip.vehicle),
            'date': trip.date.strftime('%Y-%m-%d'),
            'from_location': trip.from_location,
            'to_location': trip.to_location,
        })

    return JsonResponse({'trips': trips_data})

def garage(request):
    vehicles = Vehicle.objects.all()
    garages = Garage.objects.filter(checked_out_at__isnull=True)
    return render(request, 'garage.html', {
        'vehicles': vehicles,
        'garages': garages
    })


def garage_list(request):
    # Get all garage records and group them by vehicle registration number
    garage_records = Garage.objects.all()
    
    # Grouping the records by vehicle registration number
    grouped_records = {}
    for record in garage_records:
        if record.vehicle.regno not in grouped_records:
            grouped_records[record.vehicle.regno] = []
        grouped_records[record.vehicle.regno].append(record)

    return render(request, 'garage.html', {'grouped_records': grouped_records})
#  Fetch vehicle and garage data
def get_vehicle_data(request):
    vehicles = Vehicle.objects.all()
    garages = Garage.objects.filter(checked_out_at__isnull=True)
    
    vehicle_data = [
        {
            'id': vehicle.id,
            'regno': vehicle.vehicle_regno,
            'model': vehicle.vehicle_model,
            'type': vehicle.vehicle_type
        } for vehicle in vehicles
    ]
    
    garage_data = [
        {
            'id': garage.id,
            'vehicleId': garage.vehicle.id,
            'issue': garage.issue_description,
            'checkedInAt': garage.checked_in_at
        } for garage in garages
    ]
    
    return JsonResponse({'vehicles': vehicle_data, 'garages': garage_data})

# Add vehicle to garage
@csrf_exempt
@require_POST
def add_to_garage(request):
    vehicle_id = request.POST.get('vehicle_id')
    issue_description = request.POST.get('issue_description')
    
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)
    
    # Create or update Garage record
    garage, created = Garage.objects.get_or_create(vehicle=vehicle, checked_out_at__isnull=True)
    if created:
        garage.issue_description = issue_description
        garage.save()
    
    return JsonResponse({'success': True})

# Check out vehicle from garage
@csrf_exempt
@require_POST
def checkout_vehicle(request):
    garage_id = request.POST.get('garage_id')
    
    try:
        garage = Garage.objects.get(id=garage_id)
    except Garage.DoesNotExist:
        return JsonResponse({'error': 'Garage record not found'}, status=404)
    
    garage.checked_out_at = timezone.now()
    garage.save()
    
    return JsonResponse({'success': True})


# Maintenance
def maintenance(request):
    vehicles = Vehicle.objects.all()
    schedules = MaintenanceSchedule.objects.all()
    now = timezone.now().date()

    # Prepare schedule data with color codes based on date proximity
    schedule_data = []
    for schedule in schedules:
        days_remaining = (schedule.maintenance_date - now).days
        if days_remaining > 60:
            color_class = 'card-green'
        elif days_remaining > 30:
            color_class = 'card-orange'
        else:
            color_class = 'card-red'
        
        schedule_data.append({
            'vehicle': schedule.vehicle,
            'service_provider': schedule.service_provider,
            'maintenance_date': schedule.maintenance_date,
            'inspection_date': schedule.inspection_date,
            'insurance_date': schedule.insurance_date,
            'speed_governor_date': schedule.speed_governor_date,
            'kenha_permit_date': schedule.kenha_permit_date,
            'days_remaining': days_remaining,
            'color_class': color_class,
        })

    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        
        vehicles = Vehicle.objects.exclude(maintenanceschedule__isnull=False)
        if search_query:
            vehicles = vehicles.filter(vehicle_regno__icontains=search_query)
    
    context = {
        'vehicles': vehicles,
        'schedules': schedule_data,
    }
    return render(request, 'maintenance.html', context)


def schedule_maintenance(request, vehicle_id):
    if request.method == 'POST':
        form = MaintenanceScheduleForm(request.POST)
        if form.is_valid():
            schedule_id = request.POST.get('schedule_id', None)
            if schedule_id:
                # Update existing schedule
                schedule = get_object_or_404(MaintenanceSchedule, id=schedule_id)
                form = MaintenanceScheduleForm(request.POST, instance=schedule)
            else:
                # Create new schedule
                form = MaintenanceScheduleForm(request.POST)
            
            if form.is_valid():
                new_schedule = form.save(commit=False)
                new_schedule.vehicle = get_object_or_404(Vehicle, id=vehicle_id)
                new_schedule.save()
                return redirect('maintenance')  # Replace with your success URL
            else:
                return render(request,'maintenance.html', {'form': form})
        else:
            return render(request, 'maintenance.html', {'form': form})
    else:
        form = MaintenanceScheduleForm()
        return render(request, 'maintenance.html', {'form': form})

def get_schedule(request):
    schedule_id = request.GET.get('schedule_id')
    schedule = get_object_or_404(MaintenanceSchedule, id=schedule_id)
    data = {
        'id': schedule.id,
        'vehicle_id': schedule.vehicle.id,
        'service_provider': schedule.service_provider,
        'maintenance_date': schedule.maintenance_date,
        'inspection_date': schedule.inspection_date,
        'insurance_date': schedule.insurance_date,
        'speed_governor_date': schedule.speed_governor_date,
        'kenha_permit_date': schedule.kenha_permit_date,
    }
    return JsonResponse(data)

def delete_schedule(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        schedule = get_object_or_404(MaintenanceSchedule, id=schedule_id)
        vehicle_id = schedule.vehicle.id  # Get the vehicle id before deletion
        schedule.delete()
        
        # Check if the vehicle has any remaining schedules
        remaining_schedules = MaintenanceSchedule.objects.filter(vehicle_id=vehicle_id).exists()

        return JsonResponse({'success': True, 'vehicle_id': vehicle_id, 'has_remaining_schedules': remaining_schedules})
    
    return JsonResponse({'success': False})
