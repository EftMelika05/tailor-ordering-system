from django.db import models
from .cart_item import CartItem


class ReadyClothCartItem(CartItem):

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE
    )

    size = models.CharField(
        max_length=20
    )

    color = models.ForeignKey(
        "products.Color",
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.product.name}"