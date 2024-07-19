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
            form.save()
            return redirect('dtms_dashboard.html')
    else:
        form = TripForm()
    return render(request, 'create_trip.html', {'form': form})

def search_drivers(request):
    query = request.GET.get('query', '')
    drivers = Driver.objects.filter(name__icontains=query).values('id', 'name')
    return JsonResponse({'drivers': list(drivers)})