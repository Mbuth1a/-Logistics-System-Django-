from django.shortcuts import render, redirect
from django.http import JsonResponse
from DTMS.forms import*

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
            return redirect('dtms_dashboard.html')
    else:
        form = LoadTripForm()
    return render(request, 'load_trip.html', {'form': form})

def trip_list_json(request):
    trips = LoadTrip.objects.all()
    data = list(trips.values('id', 'trip', 'product__product', 'product__description', 'pieces', 'total_weight'))
    return JsonResponse({'trips': data})

def product_list_json(request):
    products = Product.objects.all()
    data = list(products.values('id', 'product', 'description', 'weight_per_metre'))
    return JsonResponse({'products': data})