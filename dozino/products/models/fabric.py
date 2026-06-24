from django.db import models


class Fabric(models.Model):

    THICKNESS_CHOICES = (
        ("thin", "نازک"),
        ("medium", "متوسط"),
        ("thick", "ضخیم"),
    )

    name = models.CharField(
        max_length=100
    )

    thickness = models.CharField(
        max_length=20,
        choices=THICKNESS_CHOICES
    )

    price_per_meter = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    width = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.name} - {self.get_thickness_display()}"