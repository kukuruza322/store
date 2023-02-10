from django.db import models


class Item(models.Model):
    currencies = (
        ("RUB", "RUB"),
        ("USD", "USD"),
        ("EUR", "EUR"),
    )
    name = models.CharField(max_length=50, verbose_name="Наименование")
    description = models.TextField(max_length=500, verbose_name="Описание")
    price = models.IntegerField(default=0, verbose_name="Цена")
    currency = models.CharField(max_length=20, choices=currencies, default="RUB", verbose_name="Валюта")
    add_date = models.DateField(auto_now_add=True, verbose_name="Дата поступления")

    def __str__(self):
        return f"{self.name}, {str(self.price)} {self.currency}"


class Cart(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0, verbose_name="Количество")
    subtotal = models.IntegerField(verbose_name="Стоимость")


class Discount(models.Model):
    customer_group = models.CharField(max_length=20, verbose_name="Статус покупателя")
    discount = models.IntegerField(verbose_name="Размер скидки")


class Country(models.Model):
    country = models.CharField(max_length=100, verbose_name="Страна", unique=True)
    tax_rate = models.IntegerField(verbose_name="Размер налога")


class Order(models.Model):
    creation_date = models.DateField(auto_now_add=True, verbose_name="Дата заказа")
    total = models.IntegerField(verbose_name="Общая стоимость")
    total_with_tax_and_sale = models.IntegerField(verbose_name="Итого")
    cart_id = models.ForeignKey(Cart, verbose_name="Список товаров", on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, verbose_name="Персональная скидка", on_delete=models.CASCADE)
    address = models.ForeignKey(Country, verbose_name="Адрес доставки", on_delete=models.CASCADE)

