from django.contrib import admin

from products.models import ReadyProduct
from products.models import ReadyProductVariant


admin.site.register(ReadyProduct)
admin.site.register(ReadyProductVariant)