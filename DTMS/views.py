from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from DTMS.forms import*
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import datetime
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dtms_dashboard(request):
    return render(request, 'dtms_dashboard.html')


def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            # Save form data and perform necessary operations
            form.save()
            return redirect('load_trip')  # Redirect to the load_trip page after successful form submission
    else:
        form = TripForm()
    
    return render(request, 'create_trip.html', {'form': form})
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
    records = Fuel.objects.values('trip__vehicle__vehicle_regno', 'trip_id', 'fuel_consumed', 'date')
    data = [{'vehicle': record['trip__vehicle__vehicle_regno'], 'id': record['trip_id'], 'fuel_consumed': record['fuel_consumed'], 'date': record['date']} for record in records]
    return JsonResponse(data, safe=False)
# Overall reports of monthly consumption per vehicle
@require_GET
def fetch_monthly_consumption(request):
    vehicle_id = request.GET.get('vehicle_id')
    month = request.GET.get('month')  # Expected format: 'YYYY-MM'

    if not vehicle_id or not month:
        return JsonResponse({'error': 'Vehicle ID and month are required'}, status=400)

    try:
        # Validate the month format
        year, month = map(int, month.split('-'))
        start_of_month = datetime.date(year, month, 1)
        end_of_month = (start_of_month.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
    except ValueError:
        return JsonResponse({'error': 'Invalid month format. Expected YYYY-MM'}, status=400)

    try:
        # Get trips for the specified vehicle and month
        trips = Trip.objects.filter(vehicle_id=vehicle_id, date__range=[start_of_month, end_of_month])
        fuel_records = Fuel.objects.filter(trip__in=trips).aggregate(total_consumption=Sum('fuel_consumed'))
        total_consumption = fuel_records['total_consumption'] or 0
    except Trip.DoesNotExist:
        return JsonResponse({'error': 'No trips found for the specified vehicle and month'}, status=404)

    return JsonResponse({'total_consumption': total_consumption})

def fetch_vehicle_list(request):
    vehicles = Vehicle.objects.all().values_list('vehicle_regno', flat=True)
    return JsonResponse(list(vehicles), safe=False)
