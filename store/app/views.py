import stripe
from django.shortcuts import render
from django.views import generic

from .models import Item


class IndexView(generic.ListView):
    template_name = 'app/index.html'
    context_object_name = 'latest_item_list'

    def get_queryset(self):
        return Item.objects.order_by('-add_date')[:10]


class DetailView(generic.DetailView):
    model = Item
    template_name = 'app/detail.html'


def buy(request, pk):
    item = Item.objects.get(pk=pk)
    session = create_checkout_session(item)
    context = {'item_id': pk,
               'session_id': session,
               }
    if request.method == "GET":
        return render(request, 'app/buy.html', context=context)
    else:
        return render(request, 'app/index.html', context=context)


def create_checkout_session(item):
    stripe.api_key = 'sk_test_51MZw3sGWkXptNC3XZjlcZQM4nRZUnhDLwhKMtPNGYhotxXKHZFksmuwxWCCN3Gp0HQCdnX6YjBbQrdQrqPXS7XOd00Ci0ku2Fk'
    product = stripe.Product.create(name=item.name,
                                    )

    price = stripe.Price.create(
                              product=product.id,
                              unit_amount=100*item.price,
                              currency=item.currency.lower(),
                            )
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price,
                    'quantity': 1,
                },
            ],
            currency=item.currency.lower(),
            mode='payment',
            success_url='http://localhost:8000/success.html',
        )
        return checkout_session.url
    except Exception as error:
        return str(error)


def success(request):
    pass


def cancel(request):
    pass