from django.shortcuts import render, redirect
from DTMS.forms import*

# Create your views here.
def dtms_dashboard(request):
    return render(request, 'dtms_dashboard.html')


def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_trip.html')
    else:
        form = TripForm()
    return render(request, 'create_trip.html', {'form': form})