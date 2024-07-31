from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from DTMS.forms import*
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import datetime
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET

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
def save_fuel(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        fuel_consumed = request.POST.get('fuel_consumed')

        trip = get_object_or_404(Trip, id=trip_id)

        # Save fuel consumption record
        Fuel.objects.create(trip=trip, fuel_consumed=fuel_consumed, date=trip.date)

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def fetch_fuel_records(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    vehicle_id = request.GET.get('vehicle')

    try:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
    except ValueError:
        start_date = None
        end_date = None

    trips = Trip.objects.all()

    if vehicle_id:
        try:
            vehicle_id = int(vehicle_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid vehicle ID'}, status=400)
    
    if start_date and end_date:
        trips = trips.filter(date__range=(start_date, end_date))
    
    trip_data = []
    for trip in trips:
        fuel_record = Fuel.objects.filter(trip=trip).first()  # Assuming one-to-one relationship
        trip_data.append({
            'id': trip.id,
            'vehicle': trip.vehicle.vehicle_regno,  # Adjust based on your actual vehicle field
            'date': trip.date,
            'from_location': trip.from_location,
            'to_location': trip.to_location,
            'fuel_consumed': fuel_record.fuel_consumed if fuel_record else 0,
        })

    return JsonResponse({'trips': trip_data})
# Overall reports of monthly consumption per vehicle
def fetch_monthly_consumption(request):
    vehicle_id = request.GET.get('vehicle')
    if not vehicle_id:
        return JsonResponse({'monthly_data': {}})

    trips = Trip.objects.filter(vehicle_id=vehicle_id)
    monthly_data = {}
    for trip in trips:
        fuel_record = Fuel.objects.filter(trip=trip).first()
        if fuel_record:
            month = fuel_record.date.strftime('%Y-%m')
            if month not in monthly_data:
                monthly_data[month] = 0
            monthly_data[month] += float(fuel_record.fuel_consumed)

    return JsonResponse({'monthly_data': monthly_data})

def fetch_vehicle_list(request):
    vehicles = Vehicle.objects.all().values('id', 'vehicle_regno')
    return JsonResponse({'vehicles': list(vehicles)})