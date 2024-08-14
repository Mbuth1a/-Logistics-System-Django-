from django.contrib import admin
from django.urls import path
from django.conf import settings
from DLMS.views  import* 
from django.conf.urls.static import static
# from DTMS import views
from DTMS import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('dashboard/',dashboard, name='dashboard'),
    path('dtms_dashboard/',views.dtms_dashboard, name='dtms_dashboard'),
    # Drivers
    path('add_driver/', add_driver, name='add_driver'),
    path('manage_driver/',manage_driver, name='manage_driver'),
    path('get_drivers/', get_drivers, name='get_drivers'),
    path('edit_driver/<int:id>/', edit_driver, name='edit_driver'),
    path('delete_driver/<int:id>/', delete_driver, name='delete_driver'),
    # Vehicles
    path('add_vehicle/',add_vehicle, name='add_vehicle'),
    path('manage_vehicle/',manage_vehicle, name='manage_vehicle'),
    path('get_vehicles/', get_vehicles, name='get_vehicles'),
    path('edit_vehicle/<int:id>/', edit_vehicle, name='edit_vehicle'),
    path('delete_vehicle/<int:id>/', delete_vehicle, name='delete_vehicle'),
    
    # TRIPS
    path('add_co_driver/', add_co_driver, name='add_co_driver'),
    path('manage_co_drivers/', manage_co_drivers, name='manage_co_drivers'),
    path('edit_codriver/<int:id>/',edit_codriver, name='edit_codriver'),
    path('delete_codriver/<int:id>/', delete_codriver, name='delete_codriver'),
    path('get_codrivers/', get_codrivers, name='get_codrivers'),
    path('reports/', reports, name='reports'),
    path('inventory/', inventory, name='inventory'),
    path('get-products/', get_products, name='get_products'),
    
    #DTMS
    
    path('', views.dtms_dashboard, name='dtms_dashboard'),
    path('create_trip/', views.create_trip, name='create_trip'), 
    path('load_trip/', views.load_trip, name='load_trip'),
    path('api/trips/', views.get_trips, name='get_trips'),
    
    # Expenses
    path('expenses/', views.expenses, name='expenses'),
    path('fetch_trips/', views.fetch_trips, name='fetch_trips'),
    path('get_trip_details/<int:trip_id>/', views.get_trip_details, name='get_trip_details'),
    path('assign_expenses/', views.assign_expenses, name='assign_expenses'),
    path('fetch_assigned_expenses/', views.fetch_assigned_expenses, name='fetch_assigned_expenses'),
    # Fuel Records
    path('fuel_records/', views.fuel, name='fuel_records'),
    path('save_fuel/', views.save_fuel, name='save_fuel'),
    path('fetch_fuel_records/', views.fetch_fuel_records, name='fetch_fuel_records'),
    path('fetch-monthly-consumption/', views.fetch_monthly_consumption, name='fetch_monthly_consumption'),
    path('fetch_vehicle_list/', views.fetch_vehicle_list, name='fetch_vehicle_list'),
    path('fetch-trips/', views.fetch_trips, name='fetch_trips'),
#    Garage
    path('garage/', views.garage, name='garage'),
    path('get_vehicle_data/', views.get_vehicle_data, name='get_vehicle_data'),
    path('add_to_garage/', views.add_to_garage, name='add_to_garage'),
    path('checkout_vehicle/', views.checkout_vehicle, name='checkout_vehicle'),
    # Maintenance page
    path('maintenance/', views.maintenance, name='maintenance'),
    path('schedule_maintenance/<int:vehicle_id>/', views.schedule_maintenance, name='schedule_maintenance'),
    path('get-schedule/', views.get_schedule, name='get_schedule'),
    path('delete_schedule/', views.delete_schedule, name='delete_schedule'),
    path('garage-history/', views.garage_list, name='garage_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)