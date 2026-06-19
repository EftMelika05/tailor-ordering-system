from django.db import models

class CartItem(models.Model):

    PRODUCT_TYPES = (
        ("ready", "آماده"),
        ("custom_tshirt", "تیشرت سفارشی"),
        ("custom_hoodie", "دورس سفارشی"),
        ("custom_pants", "شلوار سفارشی"),
    )

    cart = models.ForeignKey(
        "Cart",
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE
    )

    product_type = models.CharField(
        max_length=30,
        choices=PRODUCT_TYPES
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    final_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # -------------------
    # READY PRODUCT
    # -------------------

    size = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    ready_color = models.ForeignKey(
        "products.Color",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ready_cart_items"
    )

    # -------------------
    # CUSTOM PRODUCT
    # -------------------

    fabric = models.ForeignKey(
        "products.Fabric",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    custom_color = models.ForeignKey(
        "products.Color",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="custom_cart_items"
    )

    sticker = models.ForeignKey(
        "products.Sticker",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
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

    LEG_TYPES = (
        ("straight", "راسته"),
        ("keshbaf", "کشباف"),
        ("kloosh", "کلوش"),
    )

    leg_type = models.CharField(
        max_length=20,
        choices=LEG_TYPES,
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
        return f"{self.product.name} ({self.quantity})"