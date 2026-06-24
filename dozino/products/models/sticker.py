from django.db import models


class Sticker(models.Model):

    name = models.CharField(max_length=100)

    file = models.FileField(
        upload_to="stickers/"
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name