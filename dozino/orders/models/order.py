from django.conf import settings
from django.db import models


class Order(models.Model):

    STATUS_CHOICES = (
        ("pending", "در انتظار پرداخت"),
        ("paid", "پرداخت شده"),
        ("processing", "در حال اماده سازی"),
        ("shipped", "ارسال شده"),
        ("completed", "تکمیل شده"),
        ("cancelled", "لغو شده"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending"
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    full_name = models.CharField(
        max_length=255
    )

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    postal_code = models.CharField(
        max_length=20
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Order #{self.id}"