from django.urls import path
from django.contrib.auth.decorators import login_required
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
    path('', login_required(cart_page, login_url='login'), name='cart'),
    path('add/tshirt/', add_tshirt_to_cart, name='add_tshirt'),  
    path('add/hoodie/', add_hoodie_to_cart, name='add_hoodie'), 
    path('add/trousers/', add_pants_to_cart, name='add_trousers'),  
    path('add/ready/', add_ready_to_cart, name='add_ready'),  
    path('remove/<int:item_id>/', login_required(remove_cart_item, login_url='login'), name='remove_cart_item'),
    path('update-quantity/', login_required(update_cart_quantity, login_url='login'), name='update_cart_quantity'),
    path('checkout/', login_required(checkout_info, login_url='login'), name='checkout_info'),
    path('payment/', login_required(payment_gateway, login_url='login'), name='payment_gateway'),
    path('checkout/payment/', login_required(checkout_payment, login_url='login'), name='checkout_payment'),
]