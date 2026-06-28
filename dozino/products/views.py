from django.http import JsonResponse
from django.shortcuts import render

from products.models import (
    Fabric,
    Sticker,
    CollarType,
    SitePrice,
    HoodType,
    ZipperType,
    LegType,
    PocketOption,
)

from products.services.pricing import calculate_dors_price,calculate_tshirt_price,calculate_trousers_price


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


def design_dors(request):

    fabrics = Fabric.objects.filter(is_active=True)
    stickers = Sticker.objects.all()
    hoods = HoodType.objects.all()
    zippers = ZipperType.objects.all()

    context = {
        "fabrics": fabrics,
        "stickers": stickers,
        "hoods": hoods,
        "zippers": zippers,
    }

    return render(
    request,
    "products/custom clothes/dors.html",
    context
)
      

def calculate_dors(request):

    fabric_id = request.GET.get("fabric")

    hood_id = request.GET.get("hood")

    zipper_id = request.GET.get("zipper")

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

    hood = HoodType.objects.get(
        id=hood_id
    )

    zipper = ZipperType.objects.get(
        id=zipper_id
    )

    if sticker_id != "0":

        sticker = Sticker.objects.get(
            id=sticker_id
        )

        sticker_price = sticker.price

    final_price = calculate_dors_price(

        fabric=fabric,

        hood=hood,

        zipper=zipper,

        sticker_price=sticker_price,

        body_height=body_height,

        body_width=body_width,

        sleeve_height=sleeve_height,

        sewing_price=site_price.hoodie_sewing_price,

    )

    return JsonResponse({
        "price": final_price
    })
    

def design_trousers(request):

    fabrics = Fabric.objects.filter(
        is_active=True
    )

    pockets = PocketOption.objects.all()

    leg_models = LegType.objects.all()

    context = {
        "fabrics": fabrics,
        "pockets": pockets,
        "leg_models": leg_models,
    }

    return render(
        request,
        "products/custom clothes/trousers.html",
        context
    )

def calculate_trousers(request):

    fabric_id = request.GET.get(
        "fabric"
    )

    pocket_id = request.GET.get(
        "pocket"
    )

    leg_model_id = request.GET.get(
        "leg"
    )

    pants_height = float(
        request.GET.get(
            "pants_height"
        )
    )


    hip_width = float(
        request.GET.get(
            "hip_width"
        )
    )

    site_price = SitePrice.objects.first()

    fabric = Fabric.objects.get(
        id=fabric_id
    )

    pocket = PocketOption.objects.get(
        id=pocket_id
    )

    leg_model = LegType.objects.get(
        id=leg_model_id
    )

    final_price = calculate_trousers_price(

        fabric=fabric,

        leg_model=leg_model,

        pocket=pocket,

        pants_height=pants_height,

        hip_width=hip_width,

        sewing_price=site_price.pants_sewing_price,

    )

    return JsonResponse({
        "price": final_price
    })