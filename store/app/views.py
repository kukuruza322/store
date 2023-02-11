import stripe
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.decorators.http import require_GET, require_POST
import random

from .models import Item, Order, Country, Discount, Cart


class IndexView(generic.ListView):
    template_name = 'app/index.html'
    context_object_name = 'latest_item_list'

    def get_queryset(self):
        return Item.objects.order_by('-add_date')[:10]


class DetailView(generic.DetailView):
    model = Item
    template_name = 'app/detail.html'


@transaction.atomic
@require_GET
def buy(request, pk):
    """
    Возвращает перенаправление на страницу оплаты напрямую, вместо возвращения session.id + переход с помощью JS
    """
    # ordered_item = Order.objects.create(cart_id, buy_amount=buy_amount, subtotal=buy_amount * selected_item.price,
                                        # discount=discount, address=country)
    # ordered_item.save()

    item = Item.objects.get(pk=pk)
    session = create_checkout_session(item)
    Cart.objects.all().delete()

    return HttpResponseRedirect(session.url)


def create_checkout_session(item):
    """
    Создает Stripe-объекты на основе количества товаров из корзины, выбранной страны и валюты.
    """
    stripe.api_key = 'sk_test_51MZw3sGWkXptNC3XZjlcZQM4nRZUnhDLwhKMtPNGYhotxXKHZFksmuwxWCCN3Gp0HQCdnX6YjBbQrdQrqPXS7XOd00Ci0ku2Fk'
    COUNTRY = random.choice(['AU', 'DE', 'FI', 'AT', 'FR'])
    SALE = 25
    TAX = 20
    CURRENCY = item.currency.lower()
    NAME = "Petr"

    tax = stripe.TaxRate.create(display_name="НДС",
                                inclusive=False,
                                percentage=TAX,
                                country=COUNTRY,
                                description=f"{COUNTRY} Sales Tax",
                                )

    customer = stripe.Customer.create(description="Default User",
                                      address={'country': COUNTRY},
                                      name=NAME,
                                      )

    product = stripe.Product.create(name=item.name,
                                    description=item.description,
                                    )

    discount = stripe.Coupon.create(percent_off=SALE,
                                    duration="once",
                                    )

    price = stripe.Price.create(
        product=product.id,
        unit_amount=100 * item.price,
        currency=item.currency.lower(),
        tax_behavior='exclusive',
    )

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price': price,
                'quantity': 1,
                'tax_rates': [tax['id']],
            },
        ],
        automatic_tax={
            # Enable this for automated calc of taxes based on chosen Dashboard settings
            'enabled': False,
        },
        currency=CURRENCY,
        discounts=[{
            'coupon': discount,
        }],
        mode='payment',
        customer=customer,
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    return checkout_session


def success(request):
    return render(request, 'app/success.html')


def cancel(request):
    return render(request, 'app/cancel.html')


@require_POST
def add(request, pk):
    amount = 1
    selected_item = Item.objects.get(pk=pk)
    if selected_item in Cart.objects.filter(pk=pk):
        Cart.objects.get(pk=pk).update(amount=amount + 1)
    else:
        item_in_cart = Cart.objects.create(item=selected_item, amount=amount, subtotal=amount*selected_item.price)
        item_in_cart.save()
    return render(request, 'app/success.html')   # вернуть другой шаблон
