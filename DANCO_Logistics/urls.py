from django.contrib import admin
from django.urls import path

from DLMS.views  import* 

# from DTMS import views
from DTMS import views


urlpatterns = [
    path('admin/', admin.site.urls),
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
    path('api/trips/', views.get_trips, name='get_trips') 
    
]
