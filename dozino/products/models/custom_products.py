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

    available_collars = models.ManyToManyField(
        "products.CollarType",
        blank=True
    )
    
    base_sewing_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0
    )

    def __str__(self):
        return self.name

class CustomHoodie(CustomProductBase):
    hood_options = models.ManyToManyField(
        HoodOption
    )
    zipper_options = models.ManyToManyField(
       ZipperOption
    )
       
    base_sewing_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0
    )
    def __str__(self):
        return self.name



class CustomPants(CustomProductBase):

    leg_types = models.ManyToManyField(
    LegType
    )

    pocket_options = models.ManyToManyField(
        PocketOption
    )

    has_pocket = models.BooleanField(default=False)
    
       
    base_sewing_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0
    )
    def __str__(self):
        return self.name
