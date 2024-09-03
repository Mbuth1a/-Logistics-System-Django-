from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse, HttpResponse
from DTMS.forms import*
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET,require_POST
import logging
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View
from .models import Trip, Expenses
from .serializers import TripSerializer, ExpensesSerializer
logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
# Create your views here.
@login_required
@user_passes_test(lambda u: u.groups.filter(name='STAFFS').exists())
def dtms_dashboard(request):
    ongoing_trips = Trip.objects.filter(status='ongoing')
    ended_trips = Trip.objects.filter(status='ended')
    
    context = {
        'ongoing_trips': ongoing_trips,
        'ended_trips': ended_trips,
    }
    return render(request, 'dtms_dashboard.html' , context)


@login_required
def create_trip(request):
    # Only fetch drivers, co_drivers, and vehicles that are not currently assigned to an ongoing trip
    drivers = Driver.objects.exclude(trip__status='ongoing').distinct()
    co_drivers = CoDriver.objects.exclude(trip__status='ongoing').distinct()
    vehicles = Vehicle.objects.exclude(trip__status='ongoing').distinct()

    # Retrieve the choices for the 'description' field from the Trip model
    description_choices = Trip._meta.get_field('description').choices

    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.day = request.POST.get('day')  # Set the day field
            trip.save()
            return redirect('load_trip')  # Replace 'load_trip' with your URL name or path
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    form = TripForm()
    return render(request, 'create_trip.html', {
        'drivers': drivers,
        'co_drivers': co_drivers,
        'vehicles': vehicles,
        'description_choices': description_choices,  # Pass the choices to the template
        'form': form
    })

def search_drivers(request):
    query = request.GET.get('query', '')
    drivers = Driver.objects.filter(name__icontains=query).values('id', 'name')
    return JsonResponse({'drivers': list(drivers)})
# Load Trip Views 


def load_trip(request):
    if request.method == 'POST':
        form = LoadTripForm(request.POST)
        if form.is_valid():
            trip = form.cleaned_data['trip']
            products = request.POST.getlist('product_ids')
            quantities = request.POST.getlist('quantities')
            weights = request.POST.getlist('weights')
            
            # Create the LoadTrip instance
            load_trip_instance = LoadTrip.objects.create(trip=trip)

            # Add products to the LoadTrip instance with quantity and weight
            for product_id, quantity, weight in zip(products, quantities, weights):
                product = Product.objects.get(id=product_id)
                LoadTripProduct.objects.create(
                    load_trip=load_trip_instance,
                    product=product,
                    quantity=quantity,
                    total_weight=weight
                )
            
            return redirect('dtms_dashboard')  # Redirect to a success page or reload the page after successful trip loading
    else:
        form = LoadTripForm()

    # Fetch trips that do not have products loaded (only empty trips)
    empty_trips = Trip.objects.exclude(id__in=LoadTripProduct.objects.values('load_trip_id'))

    # Fetch all products for the dropdown
    products = Product.objects.all()

    context = {
        'form': form,
        'trips': empty_trips,  # Only empty trips are passed to the template
        'products': products
    }

    return render(request, 'load_trip.html', context)

def trip_products(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    products = LoadTripProduct.objects.filter(trip=trip).select_related('product')
    products_data = [{
        'product_name': p.product.product,
        'quantity': p.quantity,
        'total_weight': p.total_weight,
    } for p in products]
    
    trip_data = {
        'vehicle': trip.vehicle,
        'driver_name': trip.driver_name,
        'co_driver_name': trip.co_driver_name,
        'date': trip.date,
        'time': trip.time,
        'description': trip.description,
        'from_location': trip.from_location,
        'to_location': trip.to_location,
        'est_distance': trip.est_distance,
        'products': products_data
    }
    
    return JsonResponse(trip_data)
def load_trip_products(request, trip_id):
    # Fetch the LoadTripProduct entries for the given trip_id
    trip = LoadTrip.objects.filter(trip_id=trip_id)
    products = LoadTripProduct.objects.filter(load_trip_id=trip_id)
    
    context = {
        'products': products,
        'trip': trip
    }
    
    return render(request, 'dtms_dashboard.html', context)

def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('dtms_dashboard')  # Assuming 'ongoing_trips' is the name of the trip listing view
    else:
        form = TripForm(instance=trip)
    
    context = {
        'form': form,
        'is_edit': True,  # You can use this in the template to determine if it is an edit
    }
    
    return render(request, 'create_trip.html', context)  # Use the same template as for creating a trip


@require_POST
def delete_trip(request, trip_id):
    try:
        trip = get_object_or_404(Trip, id=trip_id)
        trip.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def end_trip(request, trip_id):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, id=trip_id)
        if trip.status == 'ongoing':
            trip.end_trip()  # Use the method defined in the model to end the trip
            return JsonResponse({'success': True, 'end_time': trip.end_time})
        else:
            return JsonResponse({'success': False, 'error': 'Trip is already ended.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
# Filtering available objects
def get_trip_data(request):
    # Fetch drivers, co_drivers, and vehicles that are not in ongoing trips
    ongoing_trips = Trip.objects.filter(status='ongoing')
    
    ongoing_drivers = ongoing_trips.values_list('driver_id', flat=True)
    ongoing_co_drivers = ongoing_trips.values_list('co_driver_id', flat=True)
    ongoing_vehicles = ongoing_trips.values_list('vehicle_id', flat=True)
    
    # Fetch vehicles that are checked in and not checked out
    checked_in_vehicles = Garage.objects.filter(
        checked_in_at__isnull=False, 
        checked_out_at__isnull=True
    ).values_list('vehicle_id', flat=True)
    
    available_drivers = Driver.objects.exclude(id__in=ongoing_drivers)
    available_co_drivers = CoDriver.objects.exclude(id__in=ongoing_co_drivers)
    available_vehicles = Vehicle.objects.exclude(id__in=ongoing_vehicles).exclude(id__in=checked_in_vehicles)
    
    # Prepare the data for JSON response
    data = {
        'drivers': [{'id': driver.id, 'name': str(driver)} for driver in available_drivers],
        'co_drivers': [{'id': co_driver.id, 'name': str(co_driver)} for co_driver in available_co_drivers],
        'vehicles': [{'id': vehicle.id, 'name': str(vehicle)} for vehicle in available_vehicles]
    }
    
    return JsonResponse(data)

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
            'stops': trip.stops,
            'to_location': trip.to_location,
            'est_distance': trip.est_distance
        } for trip in trips
    ]
    return JsonResponse(data, safe=False)

# Expenses
def expenses(request):
    return render(request, 'expenses.html')


# API'S to handle expenses data
class TripListView(APIView):
    def get(self, request):
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    
def fetch_trips(request):
    assigned_trip_ids = Expenses.objects.values_list('trip_id', flat=True)
    trips = Trip.objects.exclude(id__in=assigned_trip_ids).values('id', 'date', 'time', 'day', 'description', 'driver', 'co_driver', 'vehicle', 'from_location', 'stops', 'to_location')
    return JsonResponse(list(trips), safe=False)

class ExpenseListView(APIView):
    def get(self, request):
        expenses = Expenses.objects.all()
        serializer = ExpensesSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpensesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def trip_detail_api(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    trip_data = {
        'id': trip.id,
        'date': trip.date,
        'time': trip.time,
        'day': trip.day,
        'description': trip.description,
        'driver': trip.driver.full_name,  
        'co_driver': trip.co_driver.co_driver_name,  
        'vehicle': trip.vehicle.vehicle_regno, 
        'from_location': trip.from_location,
        'stops': trip.stops,
        'to_location': trip.to_location,
        'est_distance': trip.est_distance
    }
    return JsonResponse(trip_data)

def expenses_list(request):
    if request.method == 'GET':
        expenses = Expenses.objects.select_related('trip').all()
        expenses_data = list(expenses.values(
            'id', 'trip__id', 'driver_expense', 'co_driver_expense', 'created_at'
        ))
        return JsonResponse(expenses_data, safe=False)
def delete_expense(request, expense_id):
    if request.method == 'DELETE':
        try:
            expense = get_object_or_404(Expenses, id=expense_id)
            expense.delete()
            return JsonResponse({'message': 'Expense deleted successfully'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)    

class AssignExpenseView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        trip_id = data.get('trip')
        driver_expense = data.get('driver_expense')
        co_driver_expense = data.get('co_driver_expense')

        # Get the trip instance
        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            return JsonResponse({'error': 'Trip not found'}, status=404)

        # Create an Expense record
        Expenses.objects.create(
            trip=trip,
            driver_expense=driver_expense,
            co_driver_expense=co_driver_expense
        )

        return JsonResponse({'success': 'Expense assigned successfully'})

# FUEL VIEWS
def fuel(request):
    trips = Trip.objects.filter(fuel__isnull=True)  # Filter trips with no fuel record
    return render(request, 'fuel_records.html', {'trips': trips})
# Saving of the fuel records to the database
@csrf_exempt
def save_fuel(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        fuel_consumed = request.POST.get('fuel_consumed')
        
        try:
            trip = Trip.objects.get(id=trip_id)
            Fuel.objects.create(
                trip=trip,
                fuel_consumed=fuel_consumed,
                date=trip.date
            )
            return JsonResponse({'success': True})
        except Trip.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Trip not found'})

def fetch_fuel_records(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    vehicle_id = request.GET.get('vehicle')
    
    trips = Trip.objects.all()

    if start_date:
        trips = trips.filter(date__gte=parse_date(start_date))
    if end_date:
        trips = trips.filter(date__lte=parse_date(end_date))
    if vehicle_id:
        trips = trips.filter(vehicle_id=vehicle_id)
    
    trip_data = []
    for trip in trips:
        fuel_record = Fuel.objects.filter(trip=trip).first()
        trip_data.append({
            'id': trip.id,
            'vehicle': str(trip.vehicle),
            'date': trip.date.strftime('%Y-%m-%d'),
            'from_location': trip.from_location,
            'to_location': trip.to_location,
            'fuel_consumed': fuel_record.fuel_consumed if fuel_record else None
        })
    
    return JsonResponse({'trips': trip_data})
# Overall reports of monthly consumption per vehicle
def fetch_monthly_consumption(request):
    vehicle_regno = request.GET.get('vehicle')  # Get the vehicle registration number from the request
    monthly_data = {}
    
    # Filter the fuel records by the vehicle registration number
    fuel_records = Fuel.objects.filter(trip__vehicle__vehicle_regno=vehicle_regno)
    
    for record in fuel_records:
        month = record.date.strftime('%Y-%m')
        if month in monthly_data:
            monthly_data[month] += record.fuel_consumed
        else:
            monthly_data[month] = record.fuel_consumed
    
    return JsonResponse({'monthly_data': monthly_data})

def fetch_vehicle_list(request):
    vehicles = Vehicle.objects.all().values('id', 'vehicle_regno')
    return JsonResponse({'vehicles': list(vehicles)})


def fetch_trips(request):
    # Get trips that don't have associated fuel records
    trips_without_fuel = Trip.objects.filter(fuel__isnull=True)

    trips_data = []
    for trip in trips_without_fuel:
        trips_data.append({
            'id': trip.id,
            'vehicle': str(trip.vehicle),
            'date': trip.date.strftime('%Y-%m-%d'),
            'from_location': trip.from_location,
            'to_location': trip.to_location,
        })

    return JsonResponse({'trips': trips_data})

def garage(request):
    vehicles = Vehicle.objects.all()
    garages = Garage.objects.filter(checked_out_at__isnull=True)
    return render(request, 'garage.html', {
        'vehicles': vehicles,
        'garages': garages
    })


def garage_list(request):
    # Get all garage records and group them by vehicle registration number
    garage_records = Garage.objects.all()
    
    # Grouping the records by vehicle registration number
    grouped_records = {}
    for record in garage_records:
        if record.vehicle.regno not in grouped_records:
            grouped_records[record.vehicle.regno] = []
        grouped_records[record.vehicle.regno].append(record)

    return render(request, 'garage.html', {'grouped_records': grouped_records})
#  Fetch vehicle and garage data
def get_vehicle_data(request):
    vehicles = Vehicle.objects.all()
    garages = Garage.objects.filter(checked_out_at__isnull=True)
    
    vehicle_data = [
        {
            'id': vehicle.id,
            'regno': vehicle.vehicle_regno,
            'model': vehicle.vehicle_model,
            'type': vehicle.vehicle_type
        } for vehicle in vehicles
    ]
    
    garage_data = [
        {
            'id': garage.id,
            'vehicleId': garage.vehicle.id,
            'issue': garage.issue_description,
            'checkedInAt': garage.checked_in_at
        } for garage in garages
    ]
    
    return JsonResponse({'vehicles': vehicle_data, 'garages': garage_data})

# Add vehicle to garage
@csrf_exempt
@require_POST
def add_to_garage(request):
    vehicle_id = request.POST.get('vehicle_id')
    issue_description = request.POST.get('issue_description')
    
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)
    
    # Create or update Garage record
    garage, created = Garage.objects.get_or_create(vehicle=vehicle, checked_out_at__isnull=True)
    if created:
        garage.issue_description = issue_description
        garage.save()
    
    return JsonResponse({'success': True})

# Check out vehicle from garage
@csrf_exempt
@require_POST
def checkout_vehicle(request):
    garage_id = request.POST.get('garage_id')
    
    try:
        garage = Garage.objects.get(id=garage_id)
    except Garage.DoesNotExist:
        return JsonResponse({'error': 'Garage record not found'}, status=404)
    
    garage.checked_out_at = timezone.now()
    garage.save()
    
    return JsonResponse({'success': True})


# Maintenance
def maintenance(request):
    vehicles = Vehicle.objects.all()
    schedules = MaintenanceSchedule.objects.all()
    now = timezone.now().date()

    # Prepare schedule data with color codes based on date proximity
    schedule_data = []
    for schedule in schedules:
        days_remaining = (schedule.maintenance_date - now).days
        days_remaining = (schedule.inspection_date - now).days
        days_remaining = (schedule.insurance_date - now).days
        days_remaining = (schedule.speed_governor_date - now).days
        days_remaining = (schedule.kenha_permit_date - now).days
        
        if days_remaining > 60:
            color_class = 'card-green'
        elif days_remaining > 30:
            color_class = 'card-orange'
        else:
            color_class = 'card-red'
        
        schedule_data.append({
            'vehicle': schedule.vehicle,
            'service_provider': schedule.service_provider,
            'maintenance_date': schedule.maintenance_date,
            'inspection_date': schedule.inspection_date,
            'insurance_date': schedule.insurance_date,
            'speed_governor_date': schedule.speed_governor_date,
            'kenha_permit_date': schedule.kenha_permit_date,
            'days_remaining': days_remaining,
            'color_class': color_class,
        })

    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        
        vehicles = Vehicle.objects.exclude(maintenanceschedule__isnull=False)
        if search_query:
            vehicles = vehicles.filter(vehicle_regno__icontains=search_query)
    
    context = {
        'vehicles': vehicles,
        'schedules': schedule_data,
    }
    return render(request, 'maintenance.html', context)


def schedule_maintenance(request, vehicle_id):
    if request.method == 'POST':
        form = MaintenanceScheduleForm(request.POST)
        if form.is_valid():
            schedule_id = request.POST.get('schedule_id', None)
            if schedule_id:
                # Update existing schedule
                schedule = get_object_or_404(MaintenanceSchedule, id=schedule_id)
                form = MaintenanceScheduleForm(request.POST, instance=schedule)
            else:
                # Create new schedule
                form = MaintenanceScheduleForm(request.POST)
            
            if form.is_valid():
                new_schedule = form.save(commit=False)
                new_schedule.vehicle = get_object_or_404(Vehicle, id=vehicle_id)
                new_schedule.save()
                return redirect('maintenance')  # Replace with your success URL
            else:
                return render(request,'maintenance.html', {'form': form})
        else:
            return render(request, 'maintenance.html', {'form': form})
    else:
        form = MaintenanceScheduleForm()
        return render(request, 'maintenance.html', {'form': form})

def get_schedule(request):
    schedule_id = request.GET.get('schedule_id')
    schedule = get_object_or_404(MaintenanceSchedule, id=schedule_id)
    data = {
        'id': schedule.id,
        'vehicle_id': schedule.vehicle.id,
        'service_provider': schedule.service_provider,
        'maintenance_date': schedule.maintenance_date,
        'inspection_date': schedule.inspection_date,
        'insurance_date': schedule.insurance_date,
        'speed_governor_date': schedule.speed_governor_date,
        'kenha_permit_date': schedule.kenha_permit_date,
    }
    return JsonResponse(data)


@require_POST
def delete_schedule(request, id):
    try:
        schedule = MaintenanceSchedule.objects.get(id=id)  # Ensure correct variable usage
        schedule.delete()
        return JsonResponse({'status': 'success'})
    except MaintenanceSchedule.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Schedule does not exist'})


# Logout
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})
    return redirect('login')