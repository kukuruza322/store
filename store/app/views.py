import stripe
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.decorators.http import require_GET, require_POST

from .models import Item, Order, Cart


@require_GET
def index(request):
    latest_item_list = Item.objects.order_by('-add_date')[:10]
    cart_count = Cart.objects.count()
    context = {'latest_item_list': latest_item_list,
               'cart_count': cart_count,
               }
    return render(request, 'app/index.html', context=context)


class DetailView(generic.DetailView):
    model = Item
    template_name = 'app/detail.html'


@transaction.atomic
@require_POST
def buy_one(request, pk):
    """
    Возвращает объект-ссылку из полученной сессии и перенаправление на страницу оплаты
    вместо
    возвращение session.id + переход с помощью JS.
    """
    item_list = Item.objects.filter(pk=pk)
    currency = item_list[0].currency
    session = create_checkout_session_many(item_list, currency=currency)
    return HttpResponseRedirect(session.url)


@transaction.atomic
@require_POST
def api_buy(request, pk):
    """
    Возвращает Session ID для API
    """
    item_list = Item.objects.filter(pk=pk)
    currency = item_list[0].currency
    session = create_checkout_session_many(item_list, currency=currency)
    context = {"session": session}
    return HttpResponse(request)


@transaction.atomic
@require_POST
def buy_all(request):
    """
    Возвращает перенаправление на страницу оплаты напрямую, вместо возвращения session.id + переход с помощью JS
    """
    item_list = Item.objects.raw('SELECT app_item.id, name, description, price, currency, amount, subtotal '
                                 'FROM app_item '
                                 'INNER JOIN app_cart ON (app_cart.item_id=app_item.id)')
    sale, tax, currency = request.POST.get("sale"), request.POST.get("tax"), request.POST.get("currency")
    session = create_checkout_session_many(item_list, sale=sale, tax=tax, currency=currency)
    Cart.objects.all().delete()
    return HttpResponseRedirect(session.url)


def create_checkout_session_many(item_list, country='RU', sale='10', tax=20, currency='rub', name='Покупатель'):
    """
    Оформить заказ на всю корзину
    """
    stripe.api_key = 'sk_test_51MZw3sGWkXptNC3XZjlcZQM4nRZUnhDLwhKMtPNGYhotxXKHZFksmuwxWCCN3Gp0HQCdnX6YjBbQrdQrqPXS7XOd00Ci0ku2Fk'
    products = []
    prices = []

    discounts = []
    if int(sale) > 0:
        discounts = [{'coupon': stripe.Coupon.create(percent_off=sale, duration="once",)}]

    customer = stripe.Customer.create(description="Default User",
                                      address={'country': country},
                                      name=name,
                                      )
    tax = stripe.TaxRate.create(display_name="НДС",
                                inclusive=False,
                                percentage=tax,
                                country=country,
                                description=f"{country} Sales Tax",
                                )
    for item in item_list:
        product = stripe.Product.create(name=f'{item.name}', description=f'{item.description}')
        products.append(product)
        prices.append(stripe.Price.create(product=product.id,
                                          unit_amount=100 * item.price,
                                          currency=item.currency.lower(),
                                          tax_behavior='exclusive',
                                          )
                      )

    checkout_session = stripe.checkout.Session.create(
        line_items=[{'price': price, 'quantity': 1, 'tax_rates': [tax['id']]} for price in prices],
        automatic_tax={
            # Enable this for automated calc of taxes based on chosen Dashboard settings
            'enabled': False,
        },
        currency=currency,  # Stripe automatic currency conversion is in BETA now. Going works great some later.
        discounts=discounts,
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
    if Cart.objects.filter(item_id=pk).exists():
        add_item = Cart.objects.get(item_id=pk)
        add_item.amount += 1
        add_item.subtotal += selected_item.price
        add_item.save()
    else:
        item_in_cart = Cart.objects.create(item=selected_item, amount=amount, subtotal=amount * selected_item.price)
        item_in_cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def history(request):
    order_list = Order.objects.all()
    context = {
        'order_list': order_list,
    }
    return render(request, 'app/history.html', context=context)


def cart(request):
    cart_list = Item.objects.raw('SELECT app_item.id, name, description, price, currency, amount, subtotal '
                                 'FROM app_item '
                                 'INNER JOIN app_cart ON (app_cart.item_id=app_item.id)')
    total = Cart.objects.all().aggregate(sum=Sum('subtotal'))
    chosen_currency = 'RUB'
    context = {
        'cart_list': cart_list,
        'total': total,
        'currency': chosen_currency,
    }
    return render(request, 'app/cart.html', context=context)


def cart_flush(request):
    Cart.objects.all().delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def about(request):
    return render(request, 'app/about.html')


def checkout(request):
    cart_list = Item.objects.raw('SELECT app_item.id, name, description, price, currency, amount, subtotal '
                                 'FROM app_item '
                                 'INNER JOIN app_cart ON (app_cart.item_id=app_item.id)')
    total = Cart.objects.all().aggregate(sum=Sum('subtotal'))
    chosen_currency = 'RUB'
    context = {
        'cart_list': cart_list,
        'total': total,
        'currency': chosen_currency,
    }
    return render(request, 'app/checkout.html', context=context)