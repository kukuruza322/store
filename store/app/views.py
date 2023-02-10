from django.http import HttpResponse, request
from django.shortcuts import render
from django.views import generic

from .models import Item

#
# def index(request):
#     return render(request, 'app/index.html')


class IndexView(generic.ListView):
    template_name = 'app/index.html'
    context_object_name = 'latest_item_list'

    def get_queryset(self):
        return Item.objects.order_by('-add_date')[:10]


class DetailView(generic.DetailView):
    model = Item
    template_name = 'app/detail.html'
