from django.db import models
from .cart_item import CartItem


class ReadyClothCartItem(CartItem):

    product = models.ForeignKey(
        "ready_products.Product",
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    size = models.CharField(
        max_length=20
    )

    color = models.ForeignKey(
        "ready_products.Color",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.product.name} - {self.size}"