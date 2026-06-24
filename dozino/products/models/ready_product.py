from django.db import models


class ReadyProduct(models.Model):

    COLLAR_TYPES = (
        ("round", "گرد"),
        ("v", "هفت"),
        ("round-v","دلبری"),
    )

    SLEEVE_TYPES = (
        ("short", "کوتاه"),
        ("long", "بلند"),
    )

    FABRIC_THICKNESS = (
        ("thin", "نازک"),
        ("medium", "متوسط"),
        ("thick", "ضخیم"),
    )

    product = models.OneToOneField(
        "Product",
        on_delete=models.CASCADE,
        related_name="ready_detail"
    )

    base_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    fabric_type = models.CharField(
        max_length=100
    )

    collar_type = models.CharField(
        max_length=20,
        choices=COLLAR_TYPES
    )

    sleeve_type = models.CharField(
        max_length=20,
        choices=SLEEVE_TYPES
    )

    fabric_thickness = models.CharField(
        max_length=20,
        choices=FABRIC_THICKNESS
    )


class ReadyProductVariant(models.Model):

    product = models.ForeignKey(
        ReadyProduct,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    color = models.ForeignKey(
        "Color",
        on_delete=models.CASCADE
    )

    size = models.CharField(max_length=20)

    stock = models.PositiveIntegerField(default=0)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )