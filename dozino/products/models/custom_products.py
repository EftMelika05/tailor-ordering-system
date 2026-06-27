from django.db import models
from .option_models import  (
    CollarType,
    HoodOption,
    ZipperOption,
    LegType,
    PocketOption
)
  
from .base import CustomProductBase


class CustomTshirt(CustomProductBase):

    available_collars = models.ManyToManyField(CollarType)

    collar_type = models.CharField(
        max_length=20,
        choices=COLLAR_TYPES
    )


class CustomHoodie(CustomProductBase):
    hood_options = models.ManyToManyField(
        HoodOption
    )
    zipper_options = models.ManyToManyField(
       ZipperOption
    )

class CustomPants(CustomProductBase):

    leg_types = models.ManyToManyField(
    LegType
    )

    pocket_options = models.ManyToManyField(
        PocketOption
    )

    has_pocket = models.BooleanField(default=False)