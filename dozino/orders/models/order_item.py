from django.db import models


class OrderItem(models.Model):

    PRODUCT_TYPES = (
        ("ready", "آماده"),
        ("custom_tshirt", "تیشرت سفارشی"),
        ("custom_hoodie", "دورس سفارشی"),
        ("custom_pants", "شلوار سفارشی"),
    )

    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        null=True
    )

    product_name = models.CharField(
        max_length=255
    )

    product_type = models.CharField(
        max_length=30,
        choices=PRODUCT_TYPES
    )

    quantity = models.PositiveIntegerField()

    final_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # -------------------
    # READY PRODUCT
    # -------------------

    size = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    ready_color = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # -------------------
    # CUSTOM PRODUCT
    # -------------------

    fabric_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    custom_color = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    sticker_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # -------------------
    # TSHIRT + HOODIE
    # -------------------

    clothing_length = models.FloatField(
        null=True,
        blank=True
    )

    clothing_width = models.FloatField(
        null=True,
        blank=True
    )

    sleeve_length = models.FloatField(
        null=True,
        blank=True
    )

    # -------------------
    # HOODIE
    # -------------------

    has_hood = models.BooleanField(
        default=False
    )

    has_zipper = models.BooleanField(
        default=False
    )

    # -------------------
    # PANTS
    # -------------------

    pants_length = models.FloatField(
        null=True,
        blank=True
    )

    waist = models.FloatField(
        null=True,
        blank=True
    )

    crotch_width = models.FloatField(
        null=True,
        blank=True
    )

    leg_type = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    has_pocket = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.product_name