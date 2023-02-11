import stripe
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_GET

from .models import Item


class IndexView(generic.ListView):
    template_name = 'app/index.html'
    context_object_name = 'latest_item_list'

    def get_queryset(self):
        return Item.objects.order_by('-add_date')[:10]


class DetailView(generic.DetailView):
    model = Item
    template_name = 'app/detail.html'


@require_GET
def buy(request, pk):
    """
    Возвращает перенаправление на страницу оплаты напрямую, вместо возвращения session.id + переход с помощью JS
    """
    item = Item.objects.get(pk=pk)
    session = create_checkout_session(item)
    print(session)
    return HttpResponseRedirect(session.url)


def create_checkout_session(item):
    """
    Создает Stripe-объекты на основе количества товаров из корзины, выбранной страны и валюты.
    """
    stripe.api_key = 'sk_test_51MZw3sGWkXptNC3XZjlcZQM4nRZUnhDLwhKMtPNGYhotxXKHZFksmuwxWCCN3Gp0HQCdnX6YjBbQrdQrqPXS7XOd00Ci0ku2Fk'
    COUNTRY = 'RU'
    SALE = 50
    CURRENCY = item.currency.lower()
    tax = stripe.TaxRate.create(display_name="Sales Tax",
                                inclusive=False,
                                percentage=20,
                                country="RU",
                                description="НДС",
                                )
    customer = stripe.Customer.create(description="Default User",
                                      address={'country': COUNTRY},
                                      )
    product = stripe.Product.create(name=item.name,
                                    description=item.description,
                                    )
    discount = stripe.Coupon.create(percent_off=SALE, duration="once")
    price = stripe.Price.create(
        product=product.id,
        unit_amount=100 * item.price,
        currency=item.currency.lower(),
        tax_behavior='exclusive',
    )
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price,
                    'quantity': 1,
                },
            ],
            automatic_tax={
                'enabled': True,
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
    except Exception as error:
        return str(error)


def success(request):
    return render(request, 'app/success.html')


def cancel(request):
    return render(request, 'app/cancel.html')
