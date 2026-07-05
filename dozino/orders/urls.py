from django.urls import path
from . import views

urlpatterns = [
    path('orders-items/', views.orders, name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]