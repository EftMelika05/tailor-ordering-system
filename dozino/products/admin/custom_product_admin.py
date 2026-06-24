from django.contrib import admin

from products.models import (
    CustomTshirt,
    CustomHoodie,
    CustomPants,
    Sticker,
    Color,
    CustomProductColor
)


admin.site.register(CustomTshirt)
admin.site.register(CustomHoodie)
admin.site.register(CustomPants)

admin.site.register(Sticker)

admin.site.register(Color)
admin.site.register(CustomProductColor)