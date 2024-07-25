from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from DTMS.forms import*
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages 
from decimal import Decimal, InvalidOperation
# Create your views here.
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


def assign_expenses(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        driver_expense = request.POST.get('driver_expense')
        co_driver_expense = request.POST.get('co_driver_expense')

        trip = get_object_or_404(Trip, id=trip_id)
        expense, created = Expense.objects.get_or_create(trip=trip)

        expense.driver_expense = driver_expense
        expense.co_driver_expense = co_driver_expense
        expense.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)