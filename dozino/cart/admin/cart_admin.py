from django.contrib import admin

from cart.models import (
    Cart,
    CustomTshirtCartItem,
)

admin.site.register(Cart)
admin.site.register(CustomTshirtCartItem)