from django.db import models


class Category(models.Model):

    GENDER_CHOICES = (
        ("male", "مردانه"),
        ("female", "زنانه"),
        ("kids"," بچه گانه"),
    )

    name = models.CharField(max_length=100)

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES
    )

    def __str__(self):
        return self.name