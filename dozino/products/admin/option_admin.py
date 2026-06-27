from django.contrib import admin

from products.models import (
    CollarType,
    LegType,
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