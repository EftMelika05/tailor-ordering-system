from django.db import models
from .cart_item import CartItem


class CustomPantsCartItem(CartItem):

    fabric = models.ForeignKey(
        "products.Fabric",
        on_delete=models.SET_NULL,
        null=True
    )

    leg = models.ForeignKey(
        "products.LegType",
        on_delete=models.SET_NULL,
        null=True
    )

    pocket = models.ForeignKey(
        "products.PocketOption",
        on_delete=models.SET_NULL,
        null=True
    )

    custom_color = models.CharField(
        max_length=30
    )

    pants_length = models.FloatField()

    waist = models.FloatField()

    hip_width = models.FloatField()

    thigh_width = models.FloatField()

    def __str__(self):
        return f"Pants #{self.id}"