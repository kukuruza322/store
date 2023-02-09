from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование")
    description = models.TextField(max_length=500, verbose_name="Описание")
    price = models.IntegerField(default=0, verbose_name="Цена")


class Order(models.Model):
    pass


class Discount(models.Model):
    pass


class Tax(models.Model):
    pass
