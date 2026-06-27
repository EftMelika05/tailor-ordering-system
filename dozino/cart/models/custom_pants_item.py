from django.db import models
from .cart_item import CartItem


class CustomPantsCartItem(CartItem):

    LEG_TYPES = (
        ("straight", "راسته"),
        ("keshbaf", "کشباف"),
        ("kloosh", "کلوش"),
    )

    fabric = models.ForeignKey(
        "products.Fabric",
        on_delete=models.SET_NULL,
        null=True
    )

    color = models.ForeignKey(
        "products.Color",
        on_delete=models.SET_NULL,
        null=True
    )

    pants_length = models.FloatField()

    waist = models.FloatField()

    hip_width = models.FloatField()

    thigh_width = models.FloatField()

    leg_type = models.CharField(
        max_length=20,
        choices=LEG_TYPES
    )

    has_pocket = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"Pants #{self.id}"