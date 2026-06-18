from django.db import models


class TimestampMixin(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomProductBase(TimestampMixin):

    product = models.OneToOneField(
        "Product",
        on_delete=models.CASCADE
    )

    measurement_guide = models.ImageField(
        upload_to="measurement-guides/"
    )

    stickers = models.ManyToManyField(
        "Sticker",
        blank=True
    )
    
    fabrics = models.ManyToManyField(
        "Fabric"
    )


    class Meta:
        abstract = True