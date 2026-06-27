from django.db import models


class Fabric(models.Model):

    name = models.CharField(
        max_length=255
    )

    price_per_meter = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    fabric_width = models.FloatField(
    default=1.1 
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name