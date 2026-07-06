from django.contrib import admin
from .models import Category, Product, Color, Size, ProductVariant, ProductImage, ProductSpecification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gender', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'is_available', 'is_active')
    list_filter = ('category', 'is_available', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'color', 'size', 'stock', 'price')
    list_filter = ('product', 'color', 'size')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'is_main')


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'spec_name', 'spec_value')