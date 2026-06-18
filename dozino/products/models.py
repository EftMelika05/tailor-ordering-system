from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=0,)
    
    def __str__(self):
        return f'{self.title}, {self.price}'
     
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images') 
    image = models.ImageField(upload_to='product-images/')
    
    