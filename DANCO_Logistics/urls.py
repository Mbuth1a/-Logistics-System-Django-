from django.contrib import admin
from django.urls import path
from django.conf import settings
from DLMS.views  import* 
from django.conf.urls.static import static
# from DTMS import views
from DTMS import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', custom_login, name='login'),
    # path('', custom_login, name='login'), 
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
    
    # Co-drivers
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
    path('api/trip_products/<int:trip_id>/products/', views.trip_products, name='trip_products'),
    path('trips/<int:trip_id>/load_trip_products/', views.load_trip_products, name='load_trip_products'),
    
    
    path('api/trips/', views.get_trips, name='get_trips'),
    path('api/trip-data/', views.get_trip_data, name='trip_data'),
    path('end-trip/<int:trip_id>/', views.end_trip, name='end_trip'),
    path('edit-trip/<int:trip_id>/', views.edit_trip, name='edit_trip'),
    path('delete-trip/<int:trip_id>/', views.delete_trip, name='delete_trip'),
    

    
    
    # Expenses
    path('expenses/', views.expenses, name='expenses'),
    path('api/trips/', views.TripListView.as_view(), name='trip-list'),  # Corrected URL for TripListView
    path('api/expenses/', views.ExpenseListView.as_view(), name='expense-list'),  # Corrected URL for ExpenseListView
    path('api/trips/<int:trip_id>/', views.trip_detail_api, name='trip_detail_api'),
    path('api/assign-expense/', views.AssignExpenseView.as_view(), name='assign_expense'),
    path('api/expenses/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('api/expenses/', views.expenses_list, name='expenses_list'),
    
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
    path('garage_history/', views.garage_history, name='garage_history'),
    path('api/garage-history/', views.get_garage_history, name='get_garage_history'),
    # Maintenance page
    path('maintenance/', views.maintenance, name='maintenance'),
    path('schedule_maintenance/<int:vehicle_id>/', views.schedule_maintenance, name='schedule_maintenance'),
    path('garage-history/', views.garage_list, name='garage_list'),
    path('delete_schedule/', views.delete_schedule, name='delete_schedule'),
    path('get_schedule/', views.get_schedule, name='get_schedule'),
    path('delete_schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('bike_parking', views.bike_parking, name='bike_parking'),
    path('delete_bike/<int:bike_id>/', views.delete_bike, name='delete_bike'),
    # logout
    path('logout/', views.logout_view, name='logout'),
    
    
    path('report_form', views.report_form, name='report_form'),
    path('generate-report/', views.GenerateReportAPIView.as_view(), name='generate-report')
    
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)