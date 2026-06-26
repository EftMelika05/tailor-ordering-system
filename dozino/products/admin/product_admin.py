from django.contrib import admin

from products.models import Product
from products.models import ProductImage


admin.site.register(Product)
admin.site.register(ProductImage)