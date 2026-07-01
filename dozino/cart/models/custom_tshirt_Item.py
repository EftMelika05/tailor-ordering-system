from django.db import models
from .cart_item import CartItem


class CustomTshirtCartItem(CartItem):

    fabric = models.ForeignKey(
        "products.Fabric",
        on_delete=models.SET_NULL,
        null=True
    )

    collar = models.ForeignKey(
        "products.CollarType",
        on_delete=models.SET_NULL,
        null=True
    )
    
    collar_style = models.CharField(
    max_length=30
    )
    
    custom_color = models.CharField(
    max_length=30
    )

    sticker = models.ForeignKey(
        "products.Sticker",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    body_height = models.FloatField()

    body_width = models.FloatField()

    sleeve_height = models.FloatField()

    def __str__(self):
        return f"Tshirt #{self.id}"