from django.db import models


class CartItem(models.Model):

    cart = models.ForeignKey(
        "cart.Cart",
        on_delete=models.CASCADE,
        related_name="%(class)s_items"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    final_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True