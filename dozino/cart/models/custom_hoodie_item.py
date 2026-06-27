from django.db import models

from .cart_item import CartItem


class CustomHoodieCartItem(CartItem):

    fabric = models.ForeignKey(
        "products.Fabric",
        on_delete=models.SET_NULL,
        null=True
    )

    color = models.CharField(
        max_length=30
    )

    has_hood = models.BooleanField(
        default=True
    )

    has_zipper = models.BooleanField(
        default=False
    )

    body_height = models.FloatField()

    body_width = models.FloatField()

    sleeve_height = models.FloatField()