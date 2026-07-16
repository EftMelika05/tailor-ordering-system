import json
import random
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    Cart,
    CustomTshirtCartItem,
    CustomHoodieCartItem,
    CustomPantsCartItem,
    ReadyClothCartItem,
    CartItem,
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
# دیکشنری ترجمه رنگ‌ها
# ============================================================
COLOR_TRANSLATION = {
    'white': 'سفید',
    'black': 'سیاه',
    'gray': 'طوسی',
    'cream': 'کرمی',
    'navy': 'سرمه‌ای',
    'brown': 'قهوه‌ای',
    'olive': 'زیتونی',
    'peach': 'گلبهی',
}


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

# ============================================================
# افزودن تیشرت به سبد خرید
# ============================================================
def add_tshirt_to_cart(request):
    # ===== بررسی لاگین =====
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "login_required"}, status=401)
    
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        
        cart, created = Cart.objects.get_or_create(user=request.user)

        fabric = Fabric.objects.get(id=data["fabric"])
        collar = CollarType.objects.get(id=data["collar"])

        sticker = None
        if data.get("sticker") and data["sticker"] != "0":
            sticker = Sticker.objects.get(id=data["sticker"])

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

        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


# ============================================================
# افزودن هودی به سبد خرید
# ============================================================
def add_hoodie_to_cart(request):
    # ===== بررسی لاگین =====
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "login_required"}, status=401)
    
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        
        cart, created = Cart.objects.get_or_create(user=request.user)

        fabric = Fabric.objects.get(id=data["fabric"])
        hood = HoodType.objects.get(id=data["hood"])
        zipper = ZipperType.objects.get(id=data["zipper"])

        sticker = None
        if data.get("sticker") and data["sticker"] != "0":
            sticker = Sticker.objects.get(id=data["sticker"])

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

        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


# ============================================================
# افزودن شلوار به سبد خرید
# ============================================================
def add_pants_to_cart(request):
    # ===== بررسی لاگین =====
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "login_required"}, status=401)
    
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    try:
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
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


# ============================================================
# افزودن محصول آماده به سبد خرید
# ============================================================
def add_ready_to_cart(request):
    # ===== بررسی لاگین =====
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "login_required"}, status=401)
    
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        
        product_id = data.get("product_id")
        size_name = data.get("size")
        color_name = data.get("color")
        quantity = int(data.get("quantity", 1))
        
        product = Product.objects.get(id=product_id)
        size = Size.objects.get(name=size_name)
        
        color = None
        if color_name:
            try:
                color = Color.objects.get(name=color_name)
            except Color.DoesNotExist:
                pass
        
        variant = ProductVariant.objects.filter(
            product=product,
            size=size,
            color=color
        ).first()
        
        if not variant:
            return JsonResponse({
                "status": "error",
                "message": "قیمت این سایز موجود نیست"
            })
        
        if variant.stock < quantity:
            return JsonResponse({"status": "error",
            "message": f"فقط {variant.stock} عدد از این محصول موجود است."})
        
        price = variant.price
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        item = ReadyClothCartItem.objects.create(
            cart=cart,
            product=product,
            size=size_name,
            color=color,
            quantity=quantity,
            final_price=price
            
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
    try:
        item = CustomTshirtCartItem.objects.get(id=item_id, cart__user=request.user)
        item.delete()
        return JsonResponse({"status": "success"})
    except CustomTshirtCartItem.DoesNotExist:
        pass

    try:
        item = CustomHoodieCartItem.objects.get(id=item_id, cart__user=request.user)
        item.delete()
        return JsonResponse({"status": "success"})
    except CustomHoodieCartItem.DoesNotExist:
        pass

    try:
        item = CustomPantsCartItem.objects.get(id=item_id, cart__user=request.user)
        item.delete()
        return JsonResponse({"status": "success"})
    except CustomPantsCartItem.DoesNotExist:
        pass
    
    try:
        item = ReadyClothCartItem.objects.get(id=item_id, cart__user=request.user)
        item.delete()
        return JsonResponse({"status": "success"})
    except ReadyClothCartItem.DoesNotExist:
        pass

    return JsonResponse({"status": "error", "message": "Item not found"})


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

    try:
        item = CustomTshirtCartItem.objects.get(id=item_id, cart__user=request.user)
    except CustomTshirtCartItem.DoesNotExist:
        pass

    if not item:
        try:
            item = CustomHoodieCartItem.objects.get(id=item_id, cart__user=request.user)
        except CustomHoodieCartItem.DoesNotExist:
            pass

    if not item:
        try:
            item = CustomPantsCartItem.objects.get(id=item_id, cart__user=request.user)
        except CustomPantsCartItem.DoesNotExist:
            pass
    
    if not item:
        try:
            item = ReadyClothCartItem.objects.get(id=item_id, cart__user=request.user)
        except ReadyClothCartItem.DoesNotExist:
            pass

    if not item:
        return JsonResponse({"status": "error", "message": "Item not found"})

    if action == "increase":

        if isinstance(item, ReadyClothCartItem):
            variant = ProductVariant.objects.filter(product=item.product,
            size__name=item.size,color=item.color).first()
            if variant and item.quantity + 1 > variant.stock:
                return JsonResponse({
                "status": "error",
                "message": f"موجودی کافی نیست. فقط {variant.stock} عدد موجود است."})
        item.quantity += 1

    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1

    if isinstance(item, ReadyClothCartItem):
        variant = ProductVariant.objects.filter(product=item.product,size__name=item.size,
        color=item.color).first()
        if variant:
          item.final_price = variant.price
    item.save()

    return JsonResponse({
        "status": "success",
        "quantity": item.quantity
    })


# ============================================================
# بررسی اطلاعات کاربر و نمایش خلاصه سفارش
# ============================================================
@login_required
def checkout_info(request):
    user = request.user
    
    missing_fields = []
    if not user.full_name:
        missing_fields.append('نام و نام خانوادگی')
    if not user.phone_number:
        missing_fields.append('شماره تماس')
    if not user.address:
        missing_fields.append('آدرس')
    if not user.postal_code:
        missing_fields.append('کد پستی')
    if not user.gender:
        missing_fields.append('جنسیت')
    
    if missing_fields:
        messages.error(request, f'لطفاً اطلاعات زیر را تکمیل کنید: {", ".join(missing_fields)}')
        return redirect('profile')
        
    cart, created = Cart.objects.get_or_create(user=user)
    
    tshirt_items = CustomTshirtCartItem.objects.filter(cart=cart)
    hoodie_items = CustomHoodieCartItem.objects.filter(cart=cart)
    pants_items = CustomPantsCartItem.objects.filter(cart=cart)
    ready_items = ReadyClothCartItem.objects.filter(cart=cart)
    
    total_price = 0
    for item in tshirt_items:
        total_price += item.final_price
    for item in hoodie_items:
        total_price += item.final_price
    for item in pants_items:
        total_price += item.final_price
    for item in ready_items:
        total_price += item.final_price
    
    context = {
        'user': user,
        'total_price': total_price,
        'tshirt_items': tshirt_items,
        'hoodie_items': hoodie_items,
        'pants_items': pants_items,
        'ready_items': ready_items,
    }
    
    return render(request, 'cart/checkout.html', context)


# ============================================================
# صفحه درگاه پرداخت
# ============================================================
@login_required
def payment_gateway(request):

    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    
    tshirt_items = CustomTshirtCartItem.objects.filter(cart=cart)
    hoodie_items = CustomHoodieCartItem.objects.filter(cart=cart)
    pants_items = CustomPantsCartItem.objects.filter(cart=cart)
    ready_items = ReadyClothCartItem.objects.filter(cart=cart)

    if not (tshirt_items.exists() or hoodie_items.exists() or
             pants_items.exists() or ready_items.exists()):
              return redirect('cart')
    
    total_price = 0
    for item in tshirt_items:
        total_price += item.final_price
    for item in hoodie_items:
        total_price += item.final_price
    for item in pants_items:
        total_price += item.final_price
    for item in ready_items:
        total_price += item.final_price
    
    order_number = random.randint(100000, 999999)
    
    context = {
        'user': user,
        'total_price': total_price,
        'order_number': order_number,
    }
    
    return render(request, 'cart/payment_gateway.html', context)


# ============================================================
# ثبت نهایی سفارش
# ============================================================
@login_required
# ============================================================
# ثبت نهایی سفارش
# ============================================================
@login_required
def checkout_payment(request):
    if request.method != 'POST':
        return redirect('cart')
    
    user = request.user
    
    if not user.full_name or not user.phone_number or not user.address:
        return redirect('profile')
    
    cart, created = Cart.objects.get_or_create(user=user)
    
    items = []
    total_price = 0
    
    # ===== تیشرت سفارشی =====
    for item in CustomTshirtCartItem.objects.filter(cart=cart):
        color_name = COLOR_TRANSLATION.get(item.custom_color, item.custom_color)
        collar_name = item.collar.name
        
        items.append({
            'product_name': 'تیشرت سفارشی', 
            'product_type': 'custom_tshirt',
            'quantity': item.quantity,
            'price': item.final_price,
            'fabric_name': item.fabric.name,
            'custom_color': color_name,
            'collar_style': collar_name,
            'clothing_length': item.body_height,
            'clothing_width': item.body_width,
            'sleeve_length': item.sleeve_height,
            'sticker_id': item.sticker.id if item.sticker else None,  
            'sticker_name': item.sticker.name if item.sticker else '', 
        })
        total_price += item.final_price
    
    # ===== هودی سفارشی =====
    for item in CustomHoodieCartItem.objects.filter(cart=cart):
        color_name = COLOR_TRANSLATION.get(item.custom_color, item.custom_color)
        
        items.append({
            'product_name': 'دورس سفارشی',  # ← فقط اسم محصول، بدون پارچه
            'product_type': 'custom_hoodie',
            'quantity': item.quantity,
            'price': item.final_price,
            'fabric_name': item.fabric.name,
            'custom_color': color_name,
            'has_hood': (item.hood.name != 'بدون کلاه'),
            'has_zipper': (item.zipper.name != 'بدون زیپ'),
            'clothing_length': item.body_height,
            'clothing_width': item.body_width,
            'sleeve_length': item.sleeve_height,
            'sticker_id': item.sticker.id if item.sticker else None,  
            'sticker_name': item.sticker.name if item.sticker else '',
        })
        total_price += item.final_price
    
    # ===== شلوار سفارشی (اصلاح شده) =====
    for item in CustomPantsCartItem.objects.filter(cart=cart):
        color_name = COLOR_TRANSLATION.get(item.custom_color, item.custom_color)
        
        items.append({
            'product_name': 'شلوار سفارشی', 
            'product_type': 'custom_pants',
            'quantity': item.quantity,
            'price': item.final_price,
            'fabric_name': item.fabric.name,
            'custom_color': color_name,
            'leg_type': item.leg.name,
            'has_pocket': (item.pocket.name != 'بدون جیب'),
            'pants_length': item.pants_length,
            'waist': item.waist,
            'hip_width': item.hip_width,      # ✅ اصلاح
            'thigh_width': item.thigh_width,  # ✅ اضافه شد
        })
        total_price += item.final_price
    
    # ===== محصولات آماده =====
    for item in ReadyClothCartItem.objects.filter(cart=cart):
        items.append({
            'product_name': item.product.name,
            'product_type': 'ready',
            'quantity': item.quantity,
            'price': item.final_price,
            'size': item.size,
            'ready_color': item.color.name if item.color else '',
            'product_id': item.product.id, 

        })
        total_price += item.final_price
    
    # ===== ایجاد سفارش =====
    from orders.models import Order, OrderItem
    
    order = Order.objects.create(
        user=user,
        full_name=user.full_name,
        phone=user.phone_number,
        address=user.address,
        postal_code=user.postal_code or '',
        total_price=total_price,
        status='paid',
    )
    
    # ===== ایجاد آیتم‌های سفارش =====
    for item in items:
        order_item_data = {
            'order': order,
            'product_name': item['product_name'],
            'product_type': item['product_type'],
            'quantity': item['quantity'],
            'final_price': item['price'],
            'fabric_name': item.get('fabric_name', ''),
            'custom_color': item.get('custom_color', ''),
        }
        
        # فیلدهای مخصوص تیشرت و هودی
        if item['product_type'] in ['custom_tshirt', 'custom_hoodie']:
            order_item_data.update({
                'collar_style': item.get('collar_style', ''),
                'clothing_length': item.get('clothing_length'),
                'clothing_width': item.get('clothing_width'),
                'sleeve_length': item.get('sleeve_length'),
                'has_hood': item.get('has_hood', False),
                'has_zipper': item.get('has_zipper', False),
                'sticker_name': item.get('sticker_name', ''),  
                'sticker_id': item.get('sticker_id'),        
            })
        
        # فیلدهای مخصوص شلوار
        elif item['product_type'] == 'custom_pants':
            order_item_data.update({
                'pants_length': item.get('pants_length'),
                'waist': item.get('waist'),
                'hip_width': item.get('hip_width'),
                'thigh_width': item.get('thigh_width'),
                'leg_type': item.get('leg_type', ''),
                'has_pocket': item.get('has_pocket', False),
            })
        
        # فیلدهای مخصوص محصول آماده
        elif item['product_type'] == 'ready':
            order_item_data.update({
                'size': item.get('size', ''),
                'ready_color': item.get('ready_color', ''),
                'product_id': item.get('product_id'),
            })
        
        OrderItem.objects.create(**order_item_data)
        # ===== کم کردن موجودی محصولات آماده =====
    for cart_item in ReadyClothCartItem.objects.filter(cart=cart):
        variant = ProductVariant.objects.filter(product=cart_item.product,
        size__name=cart_item.size,
        color=cart_item.color).first()
        if variant:
        # برای اطمینان دوباره موجودی را چک کن
            if variant.stock < cart_item.quantity:
               messages.error(request,f"موجودی {cart_item.product.name} کافی نیست.")
               return redirect("cart")
            variant.stock -= cart_item.quantity
            variant.save()
    
    # ===== خالی کردن سبد خرید =====
    CustomTshirtCartItem.objects.filter(cart=cart).delete()
    CustomHoodieCartItem.objects.filter(cart=cart).delete()
    CustomPantsCartItem.objects.filter(cart=cart).delete()
    ReadyClothCartItem.objects.filter(cart=cart).delete()
    
    return redirect('order_detail', order_id=order.id)