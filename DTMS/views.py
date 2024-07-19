from django.shortcuts import render, redirect
from django.http import JsonResponse
from DTMS.forms import*
from django.views.decorators.csrf import csrf_exempt
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



def load_trip(request):
    if request.method == 'POST':
        form = LoadTripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('load_trip')
    else:
        form = LoadTripForm()
    
    products = Product.objects.all()
    return render(request, 'load_trip.html', {'form': form, 'products': products})


def load_trip_view(request):
    if request.method == 'POST':
        form = LoadTripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('load_trip')
    else:
        form = LoadTripForm()
    
    products = Product.objects.all()
    trips = Trip.objects.all()
    return render(request, 'load_trip.html', {'form': form, 'products': products, 'trips': trips})

def trip_list_json(request):
    trips = LoadTrip.objects.all().select_related('product', 'trip')
    trip_list = list(trips.values(
        'id', 'trip__from_location', 'trip__to_location', 'product__name', 'product__description', 'pieces', 'rolls', 'total_weight'
    ))
    return JsonResponse({'trips': trip_list})

@csrf_exempt
def load_trip(request):
    if request.method == 'POST':
        form = LoadTripForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})