from django.db import models


# Create your models here.
class Client(models.Model):
    name = models.CharField("Имя", max_length=20)
    phone = models.IntegerField("Телефон", unique=True)
    ban = models.BooleanField()
    history = models.TextField("История клиента", blank=True)

    def __str__(self):
        return self.name.__str__() + str(self.phone)

    def getname(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Booked(models.Model):
    datetime = models.DateTimeField('Дата бронирования', unique=True)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL, blank=True)
    comment = models.TextField('Комментарий', blank=True)

    def __str__(self):
        return self.datetime.__str__()

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Бронирование"
