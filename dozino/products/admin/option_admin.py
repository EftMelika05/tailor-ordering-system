from django.contrib import admin

from products.models import (
    CollarType,
    LegType,
    HoodType,
    ZipperType,
)


@admin.register(CollarType)
class CollarTypeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "extra_price",
    )


@admin.register(LegType)
class LegTypeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "extra_price",
        
    )
    

@admin.register(HoodType)
class HoodTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "extra_price",
        "slug",
    )
 
@admin.register(ZipperType)   
class ZipperTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "extra_price",
        "slug",
    )