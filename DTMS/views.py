from django.shortcuts import render, redirect
from django.http import JsonResponse
from DTMS.forms import*
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
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

def load_trip(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip')
        product_id = request.POST.get('product')
        quantity_str = request.POST.get('quantity')
        load_type = request.POST.get('type')

        # Check if all required fields are provided
        if not all([trip_id, product_id, quantity_str, load_type]):
            messages.error(request, 'Missing required fields.')  # Use messages for errors
            return render(request, 'load_trip.html')

        # Convert quantity to float and handle potential conversion error
        try:
            quantity = float(quantity_str)
        except (ValueError, TypeError):
            messages.error(request, 'Invalid quantity value.')
            return render(request, 'load_trip.html')

        # Fetch related objects
        try:
            trip = Trip.objects.get(pk=trip_id)
            product = Product.objects.get(pk=product_id)
        except Trip.DoesNotExist:
            messages.error(request, 'Trip not found.')
            return render(request, 'load_trip.html')
        except Product.DoesNotExist:
            messages.error(request, 'Product not found.')
            return render(request, 'load_trip.html')

        # Create and save new LoadTrip instance
        load_trip = LoadTrip(
            trip=trip,
            product=product,
            quantity=quantity,
            type=load_type
        )
        load_trip.save()

        messages.success(request, 'Load trip created successfully.')
        return render(request, 'load_trip.html')  # Redirect to same page after success

    # Fetch all trips and products (consider pagination for large datasets)
    trips = Trip.objects.all()
    products = Product.objects.all()

    context = {
        'trips': trips,
        'products': products,
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