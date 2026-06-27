from django.db import models


class Sticker(models.Model):

    name = models.CharField(max_length=100)

    svg_file = models.FileField(
        upload_to="stickers/",
        blank=True,
        null=True,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name