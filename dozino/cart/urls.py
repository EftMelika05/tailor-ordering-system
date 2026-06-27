from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.cart_page,
        name="cart"
    ),

    path(
        'add/tshirt/',
        views.add_tshirt_to_cart,
        name='add_tshirt_to_cart'
    ),

]