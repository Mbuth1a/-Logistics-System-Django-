from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from DTMS.forms import*
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import datetime
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET,require_POST

# Create your views here.
def dtms_dashboard(request):
    return render(request, 'dtms_dashboard.html')


def create_trip(request):
    drivers = Driver.objects.all()
    co_drivers = CoDriver.objects.all()
    vehicles = Vehicle.objects.all()
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            # Save form data and perform necessary operations
            form.save()
            return redirect('load_trip')  # Redirect to the load_trip page after successful form submission
    else:
        form = TripForm()
    
    return render(request, 'create_trip.html', 
        {
        'drivers': drivers,
        'co_drivers': co_drivers,
        'vehicles': vehicles})
def search_drivers(request):
    query = request.GET.get('query', '')
    drivers = Driver.objects.filter(name__icontains=query).values('id', 'name')
    return JsonResponse({'drivers': list(drivers)})

# Load Trip Views 

@csrf_protect
def load_trip(request):
    if request.method == 'POST':
        trip_id = request.POST['trip']
        products = request.POST.getlist('products[]')
        types = request.POST.getlist('types[]')
        quantities = request.POST.getlist('quantities[]')
        
        trip = Trip.objects.get(id=trip_id)
        
        for product_id, type_, quantity in zip(products, types, quantities):
            product = Product.objects.get(id=product_id)
            weight = product.weight_per_metre * float(quantity)
            
            LoadTrip.objects.create(
                trip=trip,
                product=product,
                type=type_,
                quantity=quantity,
                total_weight=weight
            )
        
        return redirect('load_trip')
    
    trips = Trip.objects.all()
    products = Product.objects.all()
    
    context = {
        'trips': trips,
        'products': products
    }
    
    return render(request, 'load_trip.html', context)


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
            'to_location': trip.to_location,
            'est_distance': trip.est_distance
        } for trip in trips
    ]
    return JsonResponse(data, safe=False)


def expenses(request):
    return render(request, 'expenses.html')

def fetch_trips(request):
    trips = Trip.objects.all()
    data = [
        {
            'id': trip.id,
            'date': trip.date.isoformat(),
            'time': trip.time.isoformat(),
            'day': trip.day,
            'description': trip.description,
            'driver': trip.driver.full_name,  # Assuming Driver model has a 'full_name' field
            'co_driver': trip.co_driver.co_driver_name,  # Assuming CoDriver model has a 'co_driver_name' field
            'vehicle': str(trip.vehicle),  # Using the __str__ representation of Vehicle
            'from_location': trip.from_location,
            'to_location': trip.to_location,
            'est_distance': trip.est_distance
        } for trip in trips
    ]
    return JsonResponse(data, safe=False)

def get_trip_details(request):
    trip_id = request.GET.get('trip_id')  # Remove the comma here
    try:
        trip = Trip.objects.get(id=trip_id)
        trip_data = {
            'id': trip.id,
            'date': trip.date.isoformat(),
            'time': trip.time.isoformat(),
            'day': trip.day,
            'description': trip.description,
            'driver': {
                'full_name': trip.driver.full_name,
            },
            'co_driver': {
                'co_driver_name': trip.co_driver.co_driver_name,
            },
            'vehicle': trip.vehicle.vehicle_regno,  # Use a string representation or a serializable field
            'from_location': trip.from_location,
            'to_location': trip.to_location,
            'est_distance': trip.est_distance,
        }
        return JsonResponse(trip_data)
    except Trip.DoesNotExist:
        return JsonResponse({'error': 'Trip not found'}, status=404)


@csrf_exempt
def assign_expenses(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        driver_expense = request.POST.get('driver_expense')
        co_driver_expense = request.POST.get('co_driver_expense')

        trip = get_object_or_404(Trip, id=trip_id)

        expense = Expenses.objects.create(
            trip=trip,
            driver_expense=driver_expense,
            co_driver_expense=co_driver_expense
        )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)

def fetch_assigned_expenses(request):
    expenses = Expenses.objects.all()
    expenses_data = []

    for expense in expenses:
        expenses_data.append({
            'trip_id': expense.trip.id,
            'vehicle': expense.trip.vehicle.vehicle_regno,
            'date': expense.trip.date,
            'from_location': expense.trip.from_location,
            'to_location': expense.trip.to_location,
            'driver_name': expense.trip.driver.full_name,
            'co_driver_name': expense.trip.co_driver.co_driver_name,
            'driver_expense': expense.driver_expense,
            'co_driver_expense': expense.co_driver_expense,
        })

    return JsonResponse(expenses_data, safe=False)


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