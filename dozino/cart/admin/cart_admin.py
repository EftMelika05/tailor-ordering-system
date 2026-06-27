from django.contrib import admin

from cart.models import (
    Cart,
    CartItem,
    CustomTshirtCartItem,
)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CustomTshirtCartItem)