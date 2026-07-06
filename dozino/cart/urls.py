from django.urls import path
from cart.views import (
    cart_page,
    add_tshirt_to_cart,
    add_hoodie_to_cart,
    add_pants_to_cart,
    remove_cart_item,
    update_cart_quantity,
    add_ready_to_cart,
    payment_gateway,
    checkout_info,
    checkout_payment,
)

urlpatterns = [
    path('', cart_page, name='cart'),
    path('add/tshirt/', add_tshirt_to_cart, name='add_tshirt'),
    path('add/hoodie/', add_hoodie_to_cart, name='add_hoodie'),
    path('add/trousers/', add_pants_to_cart, name='add_trousers'),
    path('add/ready/', add_ready_to_cart, name='add_ready'),
    path('remove/<int:item_id>/', remove_cart_item, name='remove_cart_item'),
    path('update-quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', checkout_info, name='checkout_info'),
    path('payment/', payment_gateway, name='payment_gateway'),
    path('checkout/payment/', checkout_payment, name='checkout_payment'),
]