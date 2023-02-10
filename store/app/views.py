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
    if request.method == "POST":
        context = {'item_id': pk,
                   }
        return render(request, 'app/buy.html', context=context)
    else:
        return render(request, 'app/index.html', context=context)


def success(request):
    pass


def cancel(request):
    pass
