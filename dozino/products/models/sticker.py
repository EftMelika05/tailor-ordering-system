from django.db import models


class Sticker(models.Model):

    name = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to="stickers/"
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name