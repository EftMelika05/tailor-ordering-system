from django.db import models

from .base import CustomProductBase


class CustomTshirt(CustomProductBase):

    COLLAR_TYPES = (
        ("round", "گرد"),
        ("v", "هفت"),
        ("round-v","دلبری"),
    )

    collar_type = models.CharField(
        max_length=20,
        choices=COLLAR_TYPES
    )


class CustomHoodie(CustomProductBase):

    has_hood = models.BooleanField(default=False)

    has_zipper = models.BooleanField(default=False)


class CustomPants(CustomProductBase):

    LEG_TYPES = (
        ("straight", "راسته"),
        ("keshbaf", "کشباف"),
        ("kloosh", "کلوش"),
    )

    leg_type = models.CharField(
        max_length=20,
        choices=LEG_TYPES
    )

    has_pocket = models.BooleanField(default=False)