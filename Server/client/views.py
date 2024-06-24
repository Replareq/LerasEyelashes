import json

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from calendar import Calendar
from datetime import datetime, timedelta
from .models import Booked, Client
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    the_tittle = "Реснички от Леры"
    return render(request, "client/home.html", context={"the_tittle": the_tittle})


def registration(request: HttpRequest, user_month: str) -> HttpResponse:
    """month_data = week in month, day in week, day = [day number, week number, {time: client, ...}]
    start month plus three"""
    all_month = ("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                 "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")
    the_tittle = "Бронирование наращивания ресниц"

    cur_month = datetime.now().month
    cur_year = datetime.now().year

    if user_month == "now":
        user_month = all_month[cur_month-1] + " " + str(cur_year)

    selected_month = all_month.index(user_month.split()[0]) + 1
    selected_year = int(user_month.split()[1])

    calendar = Calendar(0)
    month = calendar.monthdays2calendar(selected_year, selected_month)

    month_data = []
    for week in month:
        month_data.append([])
        for day in week:
            book_day = Booked.objects.filter(datetime__year=selected_year,
                                             datetime__month=selected_month,
                                             datetime__day=day[0])
            month_data[-1].append([day[0], day[1],
                                   {item.datetime.time: item.client for item in book_day
                                    if item.datetime > datetime.today() + timedelta(days=0.5)}])

    return render(request, "client/book.html", context={"the_tittle": the_tittle,
                                                        "month_data": month_data,
                                                        "all_months": [i_month + " " + str(cur_year)
                                                                       for i_month in
                                                                       all_month[datetime.now().month - 1:]] +
                                                                      [i_month + " " + str(cur_year+1)
                                                                       for i_month in
                                                                       all_month[:datetime.now().month - 1]],
                                                        "selected_month": all_month[selected_month - 1] +
                                                                        " " + str(selected_year),
                                                        "selected_year": str(selected_year),
                                                        })
