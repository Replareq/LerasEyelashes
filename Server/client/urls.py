from django.urls import path, re_path
from . import views

urlpatterns = [
    path('book/<str:user_month>', views.registration, name="registration"),
    path('manager/loging_in/', views.manager_logged_in, name="manager_loging_in"),
    path('manager/loging_out/', views.manager_logged_out, name="manager_loging_out"),
    path('manager/add_client/', views.manager_add_client, name="manager_add_client"),
    path('manager/remove_client/', views.manager_remove_clients, name="manager_remove_client"),
    path('manager/change_client/', views.manager_change_client, name="manager_change_client"),
    path('manager/add_booking/', views.manager_add_booking, name="manager_add_booking"),
    path('manager/remove_booking/', views.manager_remove_booking, name="manager_remove_booking"),
    path('manager/clients_table', views.manager_clients_table, name="manager_clients_table"),
    path('manager/booking_table', views.manager_booking_table, name="manager_booking_table"),
    path('manager/booking_calendar', views.manager_calendar, name="manager_calendar"),
    path('', views.home, name="home"),
]
