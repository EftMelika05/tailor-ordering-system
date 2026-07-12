from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    gender_choice = (
        ("male", "مردانه"),
        ("female", "زنانه"),
        ("kids", "بچه‌گانه"),
    )
    name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=20,
        choices=gender_choice
    )
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    price = models.PositiveIntegerField()
    old_price = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    base_price = models.PositiveIntegerField(default=0, help_text="قیمت پایه محصول")
    discount_percent = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)  # #FF5733
    
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=20) 
    
    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(blank=True, null=True)
    
    class Meta:
        unique_together = ['product', 'color', 'size']
    
    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.product.name} - تصویر"

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    spec_name = models.CharField(max_length=100)  # جنس پارچه، ضخامت، مدل یقه
    spec_value = models.CharField(max_length=200)  # تریکو درجه یک، متوسط، گرد
    
    class Meta:
        unique_together = ['product', 'spec_name']
    
    def __str__(self):
        return f"{self.product.name} - {self.spec_name}: {self.spec_value}"
    