from django.db import models


class CollarType(models.Model):

    name = models.CharField(
        max_length=255
    )

    extra_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.name
   
class HoodType(models.Model):

    name = models.CharField(max_length=255)

    slug = models.CharField(max_length=50)

    extra_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.name
    
class ZipperType(models.Model):

    name = models.CharField(max_length=255)

    slug = models.CharField(max_length=50)

    extra_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.name
    
 
class LegType(models.Model):

    name = models.CharField(
        max_length=255
    )

    extra_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.name
    
class PocketOption(models.Model):

    name = models.CharField(
        max_length=255
    )

    extra_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.name