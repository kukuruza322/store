from django.db import models


class Item(models.Model):
    """
    Описание товара.
    """
    currencies = (
        ("RUB", "RUB"),
        ("USD", "USD"),
        ("EUR", "EUR"),
    )
    name = models.CharField(max_length=50, verbose_name="Наименование")
    description = models.TextField(max_length=500, verbose_name="Описание")
    price = models.DecimalField(default=0, max_digits=6, decimal_places=0, verbose_name="Цена")
    currency = models.CharField(max_length=20, choices=currencies, default="RUB", verbose_name="Валюта")
    add_date = models.DateField(auto_now_add=True, verbose_name="Дата поступления")
    stock_amount = models.IntegerField(default=0, verbose_name="Количество на складе")

    def __str__(self):
        return f"{self.name}, {str(self.price)} {self.currency}"


class Discount(models.Model):
    customer_group = models.CharField(max_length=20, verbose_name="Статус покупателя")
    discount = models.IntegerField(verbose_name="Размер скидки")


class Country(models.Model):
    """
    Модель "Country" вместо предлагаемой "Tax" для возможности пересчета ставки налога в процессе оплаты
    в зависимости от страны респондента.
    """
    country = models.CharField(max_length=100, verbose_name="Страна", unique=True)
    tax_rate = models.IntegerField(verbose_name="Размер налога")


class Order(models.Model):
    """
    Модель для добавления товаров и подготовки списка товаров к оформлению заказа.
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buy_amount = models.IntegerField(default=0, verbose_name="Количество")
    discount = models.ForeignKey(Discount, verbose_name="Персональная скидка", on_delete=models.CASCADE)
    address = models.ForeignKey(Country, verbose_name="Адрес доставки", on_delete=models.CASCADE)

