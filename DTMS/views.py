from django.shortcuts import render, redirect
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
        trip_id = request.POST.get('trip')
        product_id = request.POST.get('product')
        type = request.POST.get('type')
        quantity = request.POST.get('quantity')

        try:
            trip = Trip.objects.get(id=trip_id)
            product = Product.objects.get(id=product_id)
            quantity = float(quantity)  # Ensure quantity is an integer
            weight_per_metre = float(product.weight_per_metre)  # Ensure weight_per_metre is a float

            # Calculate total weight
            total_weight = Decimal(quantity) * Decimal(weight_per_metre)

            load_trip = LoadTrip(
                trip=trip,
                product=product,
                type=type,
                quantity=quantity,
                total_weight=total_weight
            )
            load_trip.save()
            return redirect('load_trip')

        except (Trip.DoesNotExist, Product.DoesNotExist):
            # Handle the case where the trip or product does not exist
            return render(request, 'load_trip.html', {
                'trips': Trip.objects.all(),
                'products': Product.objects.all(),
                'error': 'Selected trip or product does not exist.'
            })
        except (ValueError, InvalidOperation):
            # Handle conversion errors
            return render(request, 'load_trip.html', {
                'trips': Trip.objects.all(),
                'products': Product.objects.all(),
                'error': 'Invalid quantity or weight data.'
            })

    trips = Trip.objects.all()
    products = Product.objects.all()
    return render(request, 'load_trip.html', {'trips': trips, 'products': products})
def get_trips(request):
    trips = Trip.objects.all()
    data = [
        {
            'id': trip.id,
            'date': trip.date.isoformat(),
            'time': trip.time.isoformat(),
            'day': trip.day,
            'description': trip.description,
            'driver': trip.driver.first_name,  # Assuming Driver model has a 'name' field
            'driver': trip.driver.last_name,  # Assuming Driver model has a 'name' field
            'co_driver': trip.co_driver.co_driver_name,  # Assuming CoDriver model has a 'name' field
            'vehicle': str(trip.vehicle),  # Using the __str__ representation of Vehicle
            'from_location': trip.from_location,
            'to_location': trip.to_location,
            'est_distance': trip.est_distance
        } for trip in trips
    ]
    return JsonResponse(data, safe=False)