import json

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from calendar import Calendar
from datetime import datetime, timedelta
# from .models import Booked, Client
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    the_tittle = "Реснички от Леры"
    return render(request, "client/home.html", context={"the_tittle": the_tittle})
