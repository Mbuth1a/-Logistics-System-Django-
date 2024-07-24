from django.shortcuts import render, redirect, get_object_or_404
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .forms import DriverForm,VehicleForm, CoDriverForm, ProductForm
from .models import Driver, Vehicle, CoDriver, Product, Product
from django.contrib import messages

# Create your views here.
def dashboard(request):
    total_drivers = Driver.objects.count()
    total_vehicles = Vehicle.objects.count()
    total_codrivers = CoDriver.objects.count()
    total_products = Product.objects.count()
    context = {
        'total_drivers': total_drivers,
        'total_vehicles': total_vehicles,
        'total_codrivers': total_codrivers,
        'total_products': total_products
    }

    return render(request, 'dashboard.html', context)

# fetches drivers to populate the list
def get_drivers(request):
    drivers = list(Driver.objects.values())
    return JsonResponse(drivers, safe=False)

# Editing of the drivers entries

# Deleting drivers entries 

# Might remove it later after considerations
@csrf_exempt
def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})





logger = logging.getLogger(__name__)

def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info('Driver added successfully.')
            return redirect('dashboard')
        else:
            logger.warning('Form is not valid.')
    else:
        form = DriverForm()
    return render(request, 'add_driver.html', {'form': form})


def manage_driver(request):
    if request.method == 'GET':
        form = DriverForm(request.GET)
        if form.is_valid():
            form.save()
        else:
            logger.warning('Form is not valid')
    else:
        form=DriverForm()
    return render(request, 'manage_driver.html', {'form':form})


def get_drivers(request):
    drivers = list(Driver.objects.all().values())
    return JsonResponse(drivers, safe=False)

@csrf_exempt
def edit_driver(request, id):
    driver = Driver.objects.get(id=id)
    if request.method =='POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})
    else:
        data ={
            'full_name': driver.full_name,
            'employee_number': driver.employee_number,
            'license_number': driver.license_number,
            'phone_number': driver.phone_number,
            'email': driver.email,
        }
        return JsonResponse(data)


@csrf_exempt
def delete_driver(request, id):
    try:
        driver = Driver.objects.get (id=id)
        driver.delete()
        return JsonResponse({'status':'success'})
    except: Driver.DoesNotExist
    return JsonResponse({'status':'error'})
        

# Views relating with vehicles
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info('Vehicle added successfully.')
            return redirect('dashboard')
        else:
            logger.warning('Form is not valid.')
    else:
        form = VehicleForm()
    return render(request, 'add_vehicle.html', {'form': form})
        
        
def manage_vehicle(request):
    if request.method == 'GET':
        form = VehicleForm(request.GET)
        if form.is_valid():
            form.save()
        else:
            logger.warning('Form is not valid')
    else:
        form=VehicleForm()
    return render(request, 'manage_vehicle.html', {'form':form})
def get_vehicles(request):
    vehicles = Vehicle.objects.all().values()
    return JsonResponse(list(vehicles), safe=False)

@csrf_exempt
def edit_vehicle(request, id):
    vehicle = Vehicle.objects.get(id=id)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})
    else:
        data = {
            'vehicle_regno': vehicle.vehicle_regno,
            'vehicle_model': vehicle.vehicle_model,
            'vehicle_type': vehicle.vehicle_type,
            'engine_number': vehicle.engine_number,
            'capacity': vehicle.capacity,
        }
        return JsonResponse(data)

@csrf_exempt
def delete_vehicle(request, id):
    try:
        vehicle = Vehicle.objects.get(id=id)
        vehicle.delete()
        return JsonResponse({'status': 'success'})
    except Vehicle.DoesNotExist:
        return JsonResponse({'status': 'error'})

# Creation of co-drivers data
def add_co_driver(request):
    if request.method == 'POST':
        form = CoDriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to a success page or another appropriate page
    else:
        form = CoDriverForm()
    return render(request, 'add_co_driver.html', {'form': form})

def manage_co_drivers(request):
    codrivers = CoDriver.objects.all()
    form = CoDriverForm()
    return render(request, 'manage_co_drivers.html', {'codrivers': codrivers, 'form': form})

@csrf_exempt
def edit_codriver(request, id):
    codriver = get_object_or_404(CoDriver, id=id)
    
    if request.method == 'POST':
        form = CoDriverForm(request.POST, instance=codriver)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})
    
    return JsonResponse({
        'id': codriver.id,
        'employee_number': codriver.employee_number,
        'co_driver_name': codriver.co_driver_name,
        'phone_number': codriver.phone_number,
        'email_address': codriver.email_address
    })

@csrf_exempt
def delete_codriver(request, id):
    codriver = get_object_or_404(CoDriver, id=id)
    
    if request.method == 'POST':
        codriver.delete()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})# Add more details for error handling if needed

def get_codrivers(request):
    codrivers = CoDriver.objects.all()
    return JsonResponse(list(codrivers.values()), safe=False)  # Return JSON-serializable data

# Reports
def reports(request):
    drivers = Driver.objects.all()
    co_drivers = CoDriver.objects.all()
    vehicles = Vehicle.objects.all()
    return render(request, 'reports.html', {
        'drivers': drivers,
        'co_drivers': co_drivers,
        'vehicles': vehicles
    })
    
def inventory(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        stock_code = request.POST.get('stock_code')
        product = request.POST.get('product')
        unit_of_measure = request.POST.get('unit_of_measure')
        weight_per_metre = request.POST.get('weight_per_metre')

        new_product = Product.objects.create(
            description=description,
            stock_code=stock_code,
            product=product,
            unit_of_measure=unit_of_measure,
            weight_per_metre=weight_per_metre
        )

        return JsonResponse({'success': True, 'product': {
            'description': new_product.description,
            'stock_code': new_product.stock_code,
            'product': new_product.product,
            'unit_of_measure': new_product.unit_of_measure,
            'weight_per_metre': new_product.weight_per_metre
        }})
    elif request.method == 'GET':
        return render(request, 'inventory.html')

    return JsonResponse({'success': False})

# Getting the list of products in the database
def get_products(request):
    products = Product.objects.all()
    product_list = [
        {
            'description': product.description,
            'stock_code': product.stock_code,
            'product': product.product,
            'unit_of_measure': product.unit_of_measure,
            'weight_per_metre': product.weight_per_metre
        } for product in products
    ]
    return JsonResponse({'products': product_list})
# TRIPS MODULE VIEWS
# def create_trip(request):
#     if request.method == "POST":
#         form = TripForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('some_success_url')  # replace 'some_success_url' with the actual success URL
#     else:
#         form = TripForm()
    
#     drivers = Driver.objects.all()
#     vehicles = Vehicle.objects.all()
    
#     context = {
#         'form': form,
#         'drivers': drivers,
#         'vehicles': vehicles,
#     }
    
#     return render(request, 'create_trip.html', context)

