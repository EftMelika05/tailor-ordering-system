from django.urls import path
from . import views

urlpatterns=[
    path('orders-items/' , views.orders , name='orders')
]