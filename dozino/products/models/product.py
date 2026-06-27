from django.db import models

from .base import TimestampMixin


class Product(TimestampMixin):

    PRODUCT_TYPES = (
        ("ready", "آماده"),
        ("custom_tshirt", "تیشرت سفارشی"),
        ("custom_hoodie", "دورس سفارشی"),
        ("custom_pants", "شلوار سفارشی"),
    )

    name = models.CharField(max_length=255)

    product_type = models.CharField(
        max_length=30,
        choices=PRODUCT_TYPES
    )

    GENDER_CHOICES = (
    ("male", "مردانه"),
    ("female", "زنانه"),
    ("kids", "بچگانه"),
)

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="products/"
    )