from django.db import models


class Color(models.Model):

    name = models.CharField(max_length=50)

    hex_code = models.CharField(
        max_length=7,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class CustomProductColor(models.Model):

    # product = models.ForeignKey(
    #     "Product",
    #     on_delete=models.CASCADE,
    #     related_name="custom_colors"
    # )

    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="custom-product-colors/"
    )

    def __str__(self):
        return f"{self.product.name} - {self.color.name}"