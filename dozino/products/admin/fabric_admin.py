from django.contrib import admin

from products.models import Fabric


@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "price_per_meter",
        "fabric_width",
    )