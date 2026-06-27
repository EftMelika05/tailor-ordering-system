import json

from django.http import JsonResponse
from django.shortcuts import render

from .models import (
    Cart,
    CustomTshirtCartItem,
)

from products.models import (
    Fabric,
    CollarType,
    Sticker,
)


def cart_page(request):

    if not request.user.is_authenticated:

        return render(
            request,
            "cart/cart.html",
            {
                "tshirt_items": []
            }
        )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    tshirt_items = (
        CustomTshirtCartItem.objects.filter(
            cart=cart
        )
    )

    context = {
        "tshirt_items": tshirt_items
    }

    return render(
        request,
        "cart/cart.html",
        context
    )

def add_tshirt_to_cart(request):

    if request.method != "POST":

        return JsonResponse({
            "status": "error"
        })

    data = json.loads(request.body)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    fabric = Fabric.objects.get(
        id=data["fabric"]
    )

    collar = CollarType.objects.get(
        id=data["collar"]
    )

    sticker = None

    if data["sticker"] != "0":

        sticker = Sticker.objects.get(
            id=data["sticker"]
        )

    CustomTshirtCartItem.objects.create(

        cart=cart,

        fabric=fabric,

        collar=collar,

        sticker=sticker,

        body_height=data["body_height"],

        body_width=data["body_width"],

        sleeve_height=data["sleeve_height"],

        quantity=data["quantity"],

        final_price=data["final_price"]

    )

    return JsonResponse({
        "status": "success"
    })