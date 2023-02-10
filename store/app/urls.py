from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('item/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('buy/<int:pk>/', views.buy, name='detail'),
    path('success/', views.success, name='success')
]