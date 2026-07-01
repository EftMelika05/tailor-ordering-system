from django.db import models


class SitePrice(models.Model):

    tshirt_sewing_price = models.PositiveIntegerField(
        default=0
    )

    hoodie_sewing_price = models.PositiveIntegerField(
        default=0
    )

    pants_sewing_price = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return "Site Prices"