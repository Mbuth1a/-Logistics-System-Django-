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
        trip_id = request.POST.get('trip')
        product_id = request.POST.get('product')
        pieces = request.POST.get('pieces')
        rolls = request.POST.get('rolls')
        total_weight = request.POST.get('total_weight')

        trip = Trip.objects.get(id=trip_id)
        product = Product.objects.get(id=product_id)

        LoadTrip.objects.create(
            trip=trip,
            product=product,
            pieces=pieces,
            rolls=rolls,
            total_weight=total_weight
        )

        return JsonResponse({'status': 'success'})

    trips = Trip.objects.all()
    products = Product.objects.all()

    return render(request, 'load_trip.html', {'trips': trips, 'products': products})


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
    trips = LoadTrip.objects.select_related('trip', 'product').all()
    trip_list = [{
        'id': trip.id,
        'trip__from_location': trip.trip.from_location,
        'trip__to_location': trip.trip.to_location,
        'product__name': trip.product.name,
        'pieces': trip.pieces,
        'rolls': trip.rolls,
        'total_weight': trip.total_weight}
        for trip in trips]
    return JsonResponse({'trips': trip_list})

@csrf_exempt
def load_trip(request):
    if request.method == 'POST':
        form = LoadTripForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})