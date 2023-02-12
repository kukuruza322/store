from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('item/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('buy/<int:pk>/', views.buy_one, name='buy'),
    path('add/<int:pk>/', views.add, name='add'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('history/', views.history, name='history'),
    path('cart/', views.cart, name='cart'),
    path('about/', views.about, name='about'),
    path('cart_flush/', views.cart_flush, name='cart_flush'),
]