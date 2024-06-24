from django.urls import path, re_path
from . import views

urlpatterns = [
    path('book/<str:user_month>', views.registration, name="registration"),
    path('', views.home, name="home"),
]
