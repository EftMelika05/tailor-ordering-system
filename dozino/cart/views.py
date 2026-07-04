import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import (
    Cart,
    CustomTshirtCartItem,
    CustomHoodieCartItem,
    CustomPantsCartItem,
    ReadyClothCartItem,
)

from products.models import (
    Fabric,
    CollarType,
    Sticker,
    HoodType,
    ZipperType,
    LegType,
    PocketOption,
)

from ready_products.models import Product, Color, Size, ProductVariant


# ============================================================
# صفحه سبد خرید
# ============================================================
@login_required
def cart_page(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    tshirt_items = CustomTshirtCartItem.objects.filter(cart=cart)
    hoodie_items = CustomHoodieCartItem.objects.filter(cart=cart)
    pants_items = CustomPantsCartItem.objects.filter(cart=cart)
    ready_items = ReadyClothCartItem.objects.filter(cart=cart)

    context = {
        "tshirt_items": tshirt_items,
        "hoodie_items": hoodie_items,
        "pants_items": pants_items,
        "ready_items": ready_items,
    }

    return render(request, "cart/cart.html", context)


@login_required
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
        
        collar_style=data["collar_style"],
        
        custom_color=data["color"],

        body_height=data["body_height"],

        body_width=data["body_width"],

        sleeve_height=data["sleeve_height"],

        quantity=data["quantity"],

        final_price=data["final_price"]

    )

    return JsonResponse({
        "status": "success"
    })
    

# ============================================================
# افزودن هودی به سبد خرید
# ============================================================
@login_required
def add_hoodie_to_cart(request):

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

    hood = HoodType.objects.get(
        id=data["hood"]
    )

    zipper = ZipperType.objects.get(
        id=data["zipper"]
    )

    sticker = None

    if data.get("sticker") and data["sticker"] != "0":

        sticker = Sticker.objects.get(
            id=data["sticker"]
        )

    CustomHoodieCartItem.objects.create(

        cart=cart,

        fabric=fabric,

        hood=hood,

        zipper=zipper,

        sticker=sticker,
        
        custom_color=data["color"],

        body_height=data["body_height"],

        body_width=data["body_width"],

        sleeve_height=data["sleeve_height"],

        quantity=data["quantity"],

        final_price=data["final_price"]

    )

    return JsonResponse({
        "status": "success"
    })


# ============================================================
# افزودن شلوار به سبد خرید
# ============================================================
@login_required
def add_pants_to_cart(request):
    if request.method != "POST":
        return JsonResponse({"status": "error"})

    data = json.loads(request.body)
    
    cart, created = Cart.objects.get_or_create(user=request.user)

    fabric = Fabric.objects.get(id=data["fabric"])
    leg = LegType.objects.get(id=data["leg"])
    pocket = PocketOption.objects.get(id=data["pocket"])

    CustomPantsCartItem.objects.create(
        cart=cart,
        fabric=fabric,
        leg=leg,
        pocket=pocket,
        custom_color=data["color"],
        pants_length=data["pants_height"],   
        waist=data["waist_width"],            
        hip_width=data["hip_width"],
        thigh_width=data["thigh_width"],
        quantity=data["quantity"],
        final_price=data["final_price"]
    )

    return JsonResponse({"status": "success"})


# ============================================================
# افزودن محصول آماده به سبد خرید
# ============================================================
@login_required
def add_ready_to_cart(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"})

    try:
        data = json.loads(request.body)
        
        product_id = data.get("product_id")
        size_name = data.get("size")
        color_name = data.get("color")
        quantity = int(data.get("quantity", 1))
        
        # پیدا کردن محصول
        product = Product.objects.get(id=product_id)
        
        # پیدا کردن سایز
        size = Size.objects.get(name=size_name)
        
        # پیدا کردن رنگ
        color = None
        if color_name:
            try:
                color = Color.objects.get(name=color_name)
            except Color.DoesNotExist:
                pass
        
        # پیدا کردن قیمت از واریانت
        variant = ProductVariant.objects.filter(
            product=product,
            size=size
        ).first()
        
        if not variant:
            return JsonResponse({
                "status": "error",
                "message": "قیمت این سایز موجود نیست"
            })
        
        price = variant.price
        
        # پیدا کردن یا ایجاد سبد خرید
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # ایجاد آیتم در سبد خرید
        item = ReadyClothCartItem.objects.create(
            cart=cart,
            product=product,
            size=size_name,
            color=color,
            quantity=quantity,
            final_price=price * quantity
        )
        
        return JsonResponse({
            "status": "success",
            "message": "محصول به سبد خرید اضافه شد",
            "item_id": item.id
        })
        
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


# ============================================================
# حذف آیتم از سبد خرید
# ============================================================
@require_POST
@login_required
def remove_cart_item(request, item_id):

    # تلاش برای حذف از تیشرت
    try:
        item = CustomTshirtCartItem.objects.get(
            id=item_id,
            cart__user=request.user
        )
        item.delete()
        return JsonResponse({"status": "success"})
    except CustomTshirtCartItem.DoesNotExist:
        pass

    # تلاش برای حذف از هودی
    try:
        item = CustomHoodieCartItem.objects.get(
            id=item_id,
            cart__user=request.user
        )
        item.delete()
        return JsonResponse({"status": "success"})
    except CustomHoodieCartItem.DoesNotExist:
        pass

    # تلاش برای حذف از شلوار
    try:
        item = CustomPantsCartItem.objects.get(
            id=item_id,
            cart__user=request.user
        )
        item.delete()
        return JsonResponse({"status": "success"})
    except CustomPantsCartItem.DoesNotExist:
        pass
    
    # تلاش برای حذف از محصولات آماده
    try:
        item = ReadyClothCartItem.objects.get(id=item_id, cart__user=request.user)
        item.delete()
        return JsonResponse({"status": "success"})
    except ReadyClothCartItem.DoesNotExist:
        pass

    return JsonResponse({
        "status": "error",
        "message": "Item not found"
    })


# ============================================================
# ویرایش تعداد آیتم در سبد خرید
# ============================================================
@require_POST
@login_required
def update_cart_quantity(request):

    data = json.loads(request.body)

    item_id = data.get("item_id")
    action = data.get("action")

    item = None

    # تلاش برای پیدا کردن در تیشرت
    try:
        item = CustomTshirtCartItem.objects.get(
            id=item_id,
            cart__user=request.user
        )
    except CustomTshirtCartItem.DoesNotExist:
        pass

    # تلاش برای پیدا کردن در هودی
    if not item:
        try:
            item = CustomHoodieCartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )
        except CustomHoodieCartItem.DoesNotExist:
            pass

    # تلاش برای پیدا کردن در شلوار
    if not item:
        try:
            item = CustomPantsCartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )
        except CustomPantsCartItem.DoesNotExist:
            pass

    
    # تلاش برای پیدا کردن در محصولات آماده
    if not item:
        try:
            item = ReadyClothCartItem.objects.get(id=item_id, cart__user=request.user)
        except ReadyClothCartItem.DoesNotExist:
            pass


    if not item:
        return JsonResponse({
            "status": "error",
            "message": "Item not found"
        })

    if action == "increase":

        item.quantity += 1

    elif action == "decrease":

        if item.quantity > 1:

            item.quantity -= 1

    item.save()

    return JsonResponse({
        "status": "success",
        "quantity": item.quantity
    })
 