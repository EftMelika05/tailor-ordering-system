from django.http import JsonResponse
from django.shortcuts import render

from products.models import (
    Fabric,
    Sticker,
    CollarType,
    SitePrice,
)

from products.services.pricing import calculate_tshirt_price


def design_T_shirt(request):

    fabrics = Fabric.objects.filter(
        is_active=True
    )

    stickers = Sticker.objects.all()

    collars = CollarType.objects.all()

    context = {
        "fabrics": fabrics,
        "stickers": stickers,
        "collars": collars,
    }

    return render(
        request,
        "products/custom clothes/T_shirt.html",
        context
    )


def calculate_tshirt(request):

    fabric_id = request.GET.get("fabric")

    collar_id = request.GET.get("collar")

    sticker_id = request.GET.get("sticker")
    sticker_price = 0
    sticker = None
    
    
    site_price = SitePrice.objects.first()

    body_height = float(
        request.GET.get("body_height")
    )

    body_width = float(
        request.GET.get("body_width")
    )

    sleeve_height = float(
        request.GET.get("sleeve_height")
    )

    fabric = Fabric.objects.get(
        id=fabric_id
    )

    collar = CollarType.objects.get(
        id=collar_id
    )

    if sticker_id != "0":
        sticker = Sticker.objects.get(id=sticker_id)
        sticker_price = sticker.price

    final_price = calculate_tshirt_price(
        fabric=fabric,
        collar=collar,
        sticker_price=sticker_price,
        body_height=body_height,
        body_width=body_width,
        sleeve_height=sleeve_height,
        sewing_price=site_price.tshirt_sewing_price,
    )

    return JsonResponse({
        "price": final_price
    })
    
def ready_mades_list(request):

    return render(
        request,
        'products/ready-made clothes/list.html'
    )