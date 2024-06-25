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

    return render(request, "client/registration.html", context={"the_tittle": the_tittle,
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


def filling_blank(request: HttpRequest) -> HttpResponse:
    day = request.GET.get("day")
    month = request.GET.get("monthYear").split()[0]
    year = request.GET.get("monthYear").split()[1]
    time = request.GET.get("time")

    all_month = ("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                 "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")

    cur_year = int(year)
    cur_day = int(day)

    cur_time = int(time.split(":")[0])

    if month in all_month:
        cur_month = all_month.index(month) + 1
    else:
        return HttpResponse("ERROR, month is not in all months")

    if request.method == "GET":
        the_tittle = "Ввод данных"

        # Заблокировать бронь в БД??
        return render(request, "client/filling_blank.html", context={"the_tittle": the_tittle,
                                                                     "book_date": (day, month, year, time),
                                                                     })
    else:
        # the_tittle = "Успешно зарегестрировались"

        user_name = request.POST.get('name')
        user_tel = int(''.join(c for c in request.POST.get('phone') if c.isdigit()))
        user_comment = request.POST.get('comment')

        try:
            client = Client.objects.get(phone=user_tel)
        except ObjectDoesNotExist:
            client = Client.objects.create(name=user_name, phone=user_tel, ban=False,
                                           history=" Добавлен " + datetime.now().strftime("%d.%m.%Y %H:%M") + ";\n")

        if client.ban:
            messages.error(request, 'Телефон забанен на сайте. Вы не можете сделать запись. '
                                    'Обратитесь к менеджеру сайта.')
            return redirect(registration, "now")

        try:
            book_day = Booked.objects.get(datetime__year=cur_year,
                                          datetime__month=cur_month,
                                          datetime__day=cur_day,
                                          datetime__hour=cur_time, )

            if book_day.client is None:
                client.history = client.history + "Записан на " + book_day.datetime.strftime("%d.%m.%Y %H:%M") + ";\n"
                client.save(update_fields=["history"])
                book_day.client = client
                book_day.comment = user_comment
                book_day.save(update_fields=["client", "comment"])

                # Проверить, а действительно ли тот клиент зарегестрирован
                messages.success(request, 'Вы успешно зарегестрированы.')
                return redirect(registration, "now")
            else:
                messages.error(request, 'Возникла ошибка. Это бронирование уже занято.')
                return redirect(registration, "now")

        except ObjectDoesNotExist:
            return HttpResponse(f"ERROR, ObjectDoesNotExist {cur_day}.{cur_month}.{cur_year} {cur_time}. POST METHOD")


def manager_contacts(request: HttpRequest) -> HttpResponse:
    the_tittle = "Контакты с менеджером"
    return render(request, "client/manager_contacts.html", context={"the_tittle": the_tittle, })


def manager_logged_in(request: HttpRequest) -> HttpResponse:
    the_tittle = "Вход на страницу менеджера"
    if request.method == "GET":
        return render(request, "client/logged_in.html", context={"the_tittle": the_tittle, "error": False})
    else:
        user_name = request.POST.get("login")
        user_password = request.POST.get("password")
        user = authenticate(username=user_name, password=user_password)
        if user is not None:
            login(request, user)
            return redirect(manager_clients_table)
        else:
            return render(request, "client/logged_in.html", context={"the_tittle": the_tittle, "error": True})


def manager_logged_out(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(manager_logged_in)


def manager_clients_table(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(manager_logged_in)

    the_tittle = "База клиентов"

    clients = Client.objects.all()

    search = request.GET.get("searchClient")
    if search is not None:
        clients = Client.objects.filter(name__icontains=search). \
            union(Client.objects.filter(phone__icontains=search)). \
            union(Client.objects.filter(history__icontains=search))

    return render(request, "client/manager_clients_table.html",
                  context={"the_tittle": the_tittle, "clients": clients, })


def manager_booking_table(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect(manager_logged_in)

    the_tittle = "База бронирования"

    booking = Booked.objects.all().order_by("datetime")

    search = request.GET.get("searchBooking")
    if search is not None:
        booking = Booked.objects.filter(datetime__icontains=search). \
            union(Booked.objects.filter(client__name__icontains=search)). \
            union(Booked.objects.filter(client__phone__icontains=search)). \
            union(Booked.objects.filter(comment__icontains=search))

    return render(request, "client/manager_booking_table.html", context={"the_tittle": the_tittle,
                                                                         "booking": booking,
                                                                         })


def manager_calendar(request: HttpRequest) -> HttpResponse:
    the_tittle = "Календарь"
    all_month = ("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                 "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")

    if request.GET.get("monthYear"):
        selected_month = all_month.index(request.GET.get("monthYear").split()[0]) + 1
        selected_year = int(request.GET.get("monthYear").split()[1])
    else:
        selected_month = datetime.now().month
        selected_year = datetime.now().year

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
                                   {item.datetime.time: item.client for item in book_day}])

    return render(request, "client/manager_calendar.html", context={"the_tittle": the_tittle,
                                                                    "selected_month": all_month[selected_month - 1],
                                                                    "selected_year": str(selected_year),
                                                                    "all_months": json.dumps(all_month),
                                                                    "month_data": month_data,
                                                                    })


def manager_add_client(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        if "clientsBlock" in request.POST:
            user_name = request.POST.get('clientAddName')
            user_tel = int(''.join(c for c in request.POST.get('clientAddTel') if c.isdigit()))
            user_ban = False if request.POST.get('clientAddBan') is None else True
            user_history = request.POST.get('clientAddHistory') + " Добавлен " + \
                           datetime.now().strftime("%d.%m.%Y %H:%M") + ";\n"

            # Check if the client exists
            try:
                client = Client.objects.get(phone=user_tel)
                messages.error(request, f"Ошибка, Клиент с номером {user_tel} уже существует: id={client.id}")
            except ObjectDoesNotExist:
                Client.objects.create(name=user_name, phone=user_tel, ban=user_ban, history=user_history)

    return redirect(manager_clients_table)


def manager_remove_clients(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        clients_remove = json.loads(request.body.decode("utf-8")).get("dataClientsRemove")
        for number in clients_remove:
            Client.objects.get(phone=int(number)).delete()
        return redirect(manager_clients_table)
    else:
        return redirect(manager_clients_table)


def manager_change_client(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        client_change = json.loads(request.body.decode("utf-8"))
        if client_change.get("nameBlock") == "changeBanClient":
            client = Client.objects.get(phone=int(client_change.get("telClient")))
            if client.ban:
                client.ban = False
                client.history += " Разблокирован " + datetime.now().strftime("%d.%m.%Y %H:%M") + ";\n"
            else:
                client.ban = True
                client.history += " Заблокирован " + datetime.now().strftime("%d.%m.%Y %H:%M") + ";\n"
            client.save()
        return redirect(manager_clients_table)
    else:
        return redirect(manager_clients_table)


def manager_add_booking(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        if "bookingBlock" in request.POST:
            times = request.POST.getlist("time")
            start_date = datetime.strptime(request.POST.get("startDate"), "%Y-%m-%d")
            end_date = datetime.strptime(request.POST.get("endDate"), "%Y-%m-%d")

            all_timedates = []

            for day in range((end_date - start_date).days + 1):
                cur_day = start_date + timedelta(days=day)
                for time in times:
                    cur_time = datetime.strptime(time, "%H:%M")
                    all_timedates.append(datetime(year=cur_day.year, month=cur_day.month, day=cur_day.day,
                                                  hour=cur_time.hour, minute=cur_time.minute, ))

            for date in all_timedates:
                try:
                    Booked.objects.create(datetime=date)
                except IntegrityError:
                    messages.error(request, f"Ошибка: дата записи {date} уже существует.")

    return redirect(manager_booking_table)


def manager_remove_booking(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        booking_remove = json.loads(request.body.decode("utf-8")).get("dataBookingRemove")
        for number in booking_remove:
            Booked.objects.get(id=int(number.replace("check", ""))).delete()
        return HttpResponse()
    else:
        return redirect(manager_booking_table)
