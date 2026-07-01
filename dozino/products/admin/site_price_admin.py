from django.contrib import admin
from products.models import SitePrice


@admin.register(SitePrice)
class SitePriceAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):

        return not SitePrice.objects.exists()