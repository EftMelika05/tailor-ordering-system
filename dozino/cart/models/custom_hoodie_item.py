from django.db import models
from .cart_item import CartItem


class CustomHoodieCartItem(CartItem):

    fabric = models.ForeignKey(
        "products.Fabric",
        on_delete=models.SET_NULL,
        null=True
    )

    hood = models.ForeignKey(
        "products.HoodType",
        on_delete=models.SET_NULL,
        null=True
    )

    zipper = models.ForeignKey(
        "products.ZipperType",
        on_delete=models.SET_NULL,
        null=True
    )

    sticker = models.ForeignKey(
        "products.Sticker",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    custom_color = models.CharField(
        max_length=30
    )

    body_height = models.FloatField()

    body_width = models.FloatField()

    sleeve_height = models.FloatField()

    def __str__(self):
        return f"Hoodie #{self.id}"