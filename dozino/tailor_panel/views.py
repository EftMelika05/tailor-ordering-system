from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import time
import base64

# ===== import از ready_products =====
from ready_products.models import Category, Product, Color, Size, ProductVariant, ProductImage, ProductSpecification

# ===== import از orders =====
from orders.models import Order, OrderItem

# ===== import از products (برای مدیریت محصولات سفارشی) =====
from products.models import Fabric, Sticker, CollarType, HoodType, ZipperType, LegType, PocketOption, SitePrice


# ================================================================
# ===== AUTH VIEWS =====
# ================================================================
def tailor_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('tailor_panel:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'به پنل خیاط خوش آمدید')
            return redirect('tailor_panel:dashboard')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')
            return redirect('tailor_panel:tailor_login')
    
    return render(request, 'tailor_panel/tailor_login.html')


def tailor_logout(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید')
    return redirect('tailor_panel:tailor_login')


# ================================================================
# ===== DASHBOARD =====
# ================================================================
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def dashboard(request):
    """پنل اصلی خیاط با لیست سفارشات"""
    all_orders = Order.objects.all().order_by('-created_at')
    
    search = request.GET.get('search')
    if search:
        all_orders = all_orders.filter(id__icontains=search)
    
    new_orders = all_orders.filter(status__in=['pending', 'paid'])
    prep_orders = all_orders.filter(status='processing')
    sent_orders = all_orders.filter(status='shipped')
    completed_orders = all_orders.filter(status='completed')
    cancelled_orders = all_orders.filter(status='cancelled')
    
    for order in all_orders:
        order.total_items = order.items.count()
        # ===== آمار محصولات آماده =====
    ready_products = Product.objects.filter(is_active=True)
    total_ready_products = ready_products.count()
    total_custom_products = (
    Fabric.objects.filter(is_active=True).count() +
    Sticker.objects.filter(is_active=True).count() +
    CollarType.objects.count() +
    HoodType.objects.count() +
    ZipperType.objects.count() +
    LegType.objects.count() +
    PocketOption.objects.count()
)

    total_stock = 0
    low_stock_count = 0
    out_of_stock_count = 0
    
    for product in ready_products:
        variants = product.variants.all()
        product_stock = sum(v.stock for v in variants)
        total_stock += product_stock
        
        if product_stock == 0:
            out_of_stock_count += 1
        elif product_stock < 5:
            low_stock_count += 1

    context = {
        'new_orders': new_orders,
        'prep_orders': prep_orders,
        'sent_orders': sent_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'all_orders': all_orders,
        'total_ready_products': total_ready_products,
        'total_custom_products': total_custom_products,
        'total_stock': total_stock,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
    }
    
    return render(request, 'tailor_panel/tailor_panel.html', context)


# ================================================================
# ===== ORDER VIEWS =====
# ================================================================
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def order_detail(request, order_id):
    """نمایش جزئیات یک سفارش"""
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all().order_by('id')
    
    context = {
        'order': order,
        'items': items,
    }
    
    return render(request, 'tailor_panel/order-datalist-tailor.html', context)


@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def update_order_status(request):
    """API برای تغییر وضعیت سفارش"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        status = data.get('status')
        
        order = get_object_or_404(Order, id=order_id)
        
        status_map = {
            'processing': 'processing',
            'shipped': 'shipped',
            'cancelled': 'cancelled',
        }
        
        if status in status_map:
            order.status = status_map[status]
            order.save()
            return JsonResponse({
                'status': 'success',
                'message': 'وضعیت سفارش با موفقیت تغییر کرد',
                'new_status': order.status
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'وضعیت نامعتبر است'
            })
            
    except Order.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'سفارش یافت نشد'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


# ================================================================
# ===== PRODUCT REGISTRATION (محصولات آماده) =====
# ================================================================
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def register_product_page(request):
    """صفحه ثبت محصول آماده"""
    
    context = {
        'title': 'ثبت محصول آماده',
    }
    
    return render(request, 'tailor_panel/registering-products.html', context)

@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
@csrf_exempt
def register_product_submit(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})

    try:
        data = json.loads(request.body)
        
        # دریافت gender
        gender = data.get('gender')
        if not gender:
            return JsonResponse({
                'status': 'error',
                'message': 'جنسیت مشخص نشده'
            }, status=400)
        
        # پیدا کردن دسته‌بندی
        try:
            category = Category.objects.get(gender=gender)
        except Category.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'دسته‌بندی با جنسیت {gender} پیدا نشد'
            }, status=400)
        
        # اعتبارسنجی نام محصول
        product_name = data.get('product_name', '').strip()
        if not product_name:
            return JsonResponse({
                'status': 'error',
                'message': 'نام محصول نمی‌تواند خالی باشد'
            }, status=400)
        
        # ساخت اسلاگ
        base_slug = slugify(product_name)
        if not base_slug:
            base_slug = 'product-' + str(int(time.time()))
        
        final_slug = base_slug
        counter = 1
        while Product.objects.filter(slug=final_slug).exists():
            final_slug = f"{base_slug}-{counter}"
            counter += 1

        discount_percent = int(data.get('discount_percent') or 0)
        base_price = int(data.get('base_price') or 0)

        if discount_percent > 0:
            old_price = base_price
            price = int(base_price * (100 - discount_percent) / 100)
        else:
            old_price = None
            price = base_price

        # ===== ایجاد محصول =====
        product = Product.objects.create(
            category=category,
            name=product_name,
            slug=final_slug,
            price=price,
            base_price=base_price,
            old_price=old_price,
            discount_percent=discount_percent,
            description=data.get('description', ''),
            is_available=True,
            is_active=True,
        )
        
        # ===== ایجاد مشخصات فنی =====
        specs = data.get('specifications', {})
        for spec_name, spec_value in specs.items():
            if spec_value and spec_value != 'نامشخص':
                ProductSpecification.objects.create(
                    product=product,
                    spec_name=spec_name,
                    spec_value=spec_value
                )
        
        # ===== ایجاد رنگ‌ها و سایزها =====
        size_prices = data.get('size_prices', {})
        colors_data = data.get('colors', [])
        
        for color_data in colors_data:
            color, _ = Color.objects.get_or_create(
                name=color_data['name'],
                defaults={'code': color_data.get('code', '#000000')}
            )
            
            inventory = color_data.get('inventory', {})
            for size_name, stock in inventory.items():
                if stock > 0:
                    size, _ = Size.objects.get_or_create(name=size_name)
                    original_price = size_prices.get(size_name, 0)
                    
                    # ===== اعمال تخفیف روی قیمت سایز =====
                    if discount_percent > 0 and original_price > 0:
                        variant_price = int(original_price * (100 - discount_percent) / 100)
                    else:
                        variant_price = original_price
                    
                    variant, created = ProductVariant.objects.get_or_create(
                        product=product,
                        color=color,
                        size=size,
                        defaults={
                            'stock': stock,
                            'price': variant_price
                        }
                    )
                    
                    if not created:
                        variant.stock = stock
                        variant.price = variant_price
                        variant.save()
        
        # ===== ذخیره تصاویر =====
        images_data = data.get('images', [])
        main_index = data.get('main_image_index', 0)
        for i, image_data in enumerate(images_data):
            try:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                file_data = ContentFile(base64.b64decode(imgstr), name=f"{product.slug}_{i}.{ext}")
                
                ProductImage.objects.create(
                    product=product,
                    image=file_data,
                    is_main=(i == main_index)
                )
            except Exception as e:
                print(f"⚠️ خطا در ذخیره تصویر {i}: {e}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'محصول با موفقیت ثبت شد',
            'product_id': product.id,
            'product_slug': product.slug
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


# ================================================================
# ===== CUSTOM PRODUCT MANAGEMENT (مدیریت محصولات سفارشی) =====
# ================================================================
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def manage_custom_products(request):
    """صفحه مدیریت قیمت‌ها"""
    fabrics = Fabric.objects.filter(is_active=True)
    stickers = Sticker.objects.filter(is_active=True)
    collars = CollarType.objects.all()
    hoods = HoodType.objects.all()
    zippers = ZipperType.objects.all()
    legs = LegType.objects.all()
    pockets = PocketOption.objects.all()
    site_price = SitePrice.objects.first()
    
    context = {
        'fabrics': fabrics,
        'stickers': stickers,
        'collars': collars,
        'hoods': hoods,
        'zippers': zippers,
        'legs': legs,
        'pockets': pockets,
        'site_price': site_price,
    }
    
    return render(request, 'tailor_panel/manage-custom-products.html', context)


# ===== FABRIC - فقط ویرایش قیمت =====
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def edit_fabric(request, fabric_id):
    """API ویرایش قیمت پارچه"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    try:
        data = json.loads(request.body)
        fabric = Fabric.objects.get(id=fabric_id)
        fabric.price_per_meter = data['price_per_meter']
        fabric.save()
        return JsonResponse({
            'status': 'success',
            'message': 'قیمت پارچه با موفقیت به‌روزرسانی شد'
        })
    except Fabric.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'پارچه یافت نشد'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# ===== STICKER =====
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def add_sticker(request):
    """API افزودن استیکر جدید با عکس"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    try:
        name = request.POST.get('name')
        price = request.POST.get('price')
        svg_file = request.FILES.get('svg_file')
        
        if not name or not price:
            return JsonResponse({'status': 'error', 'message': 'نام و قیمت الزامی است'})
        
        sticker = Sticker.objects.create(
            name=name,
            price=price,
            svg_file=svg_file,
            is_active=True
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'استیکر با موفقیت اضافه شد',
            'id': sticker.id,
            'name': sticker.name,
            'price': str(sticker.price),
            'svg_url': sticker.svg_file.url if sticker.svg_file else None
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def update_sticker(request, sticker_id):
    """API ویرایش قیمت استیکر (بدون فایل)"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    try:
        data = json.loads(request.body)
        sticker = Sticker.objects.get(id=sticker_id)
        sticker.price = data['price']
        sticker.save()
        return JsonResponse({
            'status': 'success',
            'message': 'قیمت استیکر با موفقیت به‌روزرسانی شد'
        })
    except Sticker.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'استیکر یافت نشد'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def delete_sticker(request, sticker_id):
    """API حذف استیکر"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    try:
        sticker = Sticker.objects.get(id=sticker_id)
        if sticker.svg_file:
            sticker.svg_file.delete(save=False)
        sticker.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'استیکر با موفقیت حذف شد'
        })
    except Sticker.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'استیکر یافت نشد'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# ===== OPTIONS - فقط ویرایش قیمت =====
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def update_option_price(request, option_type, option_id):
    """API ویرایش قیمت گزینه اضافی"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    try:
        data = json.loads(request.body)
        
        models = {
            'collar': CollarType,
            'hood': HoodType,
            'zipper': ZipperType,
            'leg': LegType,
            'pocket': PocketOption,
        }
        
        model = models.get(option_type)
        if not model:
            return JsonResponse({'status': 'error', 'message': 'نوع گزینه نامعتبر است'})
        
        option = model.objects.get(id=option_id)
        option.extra_price = data['extra_price']
        option.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'قیمت با موفقیت به‌روزرسانی شد'
        })
        
    except model.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'گزینه یافت نشد'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# ===== SITE PRICES =====
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def update_site_prices(request):
    """API ویرایش مزد دوخت"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    try:
        data = json.loads(request.body)
        site_price, created = SitePrice.objects.get_or_create(id=1)
        
        if 'tshirt_sewing_price' in data:
            site_price.tshirt_sewing_price = data['tshirt_sewing_price']
        if 'hoodie_sewing_price' in data:
            site_price.hoodie_sewing_price = data['hoodie_sewing_price']
        if 'pants_sewing_price' in data:
            site_price.pants_sewing_price = data['pants_sewing_price']
        
        site_price.save()
        return JsonResponse({
            'status': 'success',
            'message': 'مزد دوخت با موفقیت به‌روزرسانی شد'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# ================================================================
# ===== PRODUCT MANAGEMENT (مدیریت محصولات آماده) =====
# ================================================================

# ===== GET PRODUCTS LIST =====
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def get_products_list(request):
    products = Product.objects.all().prefetch_related('variants', 'images', 'specifications').order_by('-id')
    
    result = []
    for product in products:
        variants = product.variants.all()
        total_stock = sum(v.stock for v in variants)
        discount_percent = product.discount_percent or 0
        
        product_images = []
        for img in product.images.all().order_by('-is_main', 'id'):
            product_images.append({
                'id': img.id,
                'image': img.image.url,
                'is_main': img.is_main
            })
        
        # ===== ساخت لیست واریانت‌ها =====
        variant_list = []
        for v in variants:
            # ===== قیمت اصلی (قبل از تخفیف) =====
            if discount_percent > 0 and v.price:
                original_price = int(v.price / (1 - discount_percent / 100))
            else:
                original_price = v.price
            
            variant_list.append({
                'id': v.id,
                'color_name': v.color.name,
                'color_code': v.color.code,
                'size_name': v.size.name,
                'stock': v.stock,
                'price': v.price,
                'original_price': original_price
            })
        
        result.append({
            'id': product.id,
            'name': product.name,
            'gender': product.category.gender,
            'price': product.price,
            'old_price': product.old_price,
            'discount_percent': product.discount_percent,
            'description': product.description,
            'base_price': product.base_price,
            'main_image': product.images.filter(is_main=True).first().image.url if product.images.filter(is_main=True).exists() else None,
            'images': product_images,
            'colors_count': variants.values('color').distinct().count(),
            'sizes_count': variants.values('size').distinct().count(),
            'stock_status': 'in-stock' if total_stock > 10 else 'low-stock' if total_stock > 0 else 'out-of-stock',
            'variants': variant_list,
            'is_active': product.is_active,
            'is_available': product.is_available,
        })
    
    return JsonResponse({'status': 'success', 'products': result})


# ===== UPDATE PRODUCT =====
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
@csrf_exempt
def update_product(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    try:
        data = json.loads(request.body)
        product = Product.objects.get(id=data['id'])
        
        # ===== به‌روزرسانی اطلاعات اصلی =====
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)

        base_price = data.get('base_price', 0)
        discount_percent = data.get('discount_percent', 0)
        
        if discount_percent > 0:
            product.old_price = base_price
            product.price = int(base_price * (100 - discount_percent) / 100)
        else:
            product.old_price = None
            product.price = base_price
        
        product.base_price = base_price
        product.discount_percent = discount_percent
        product.save()
        
        # ===== دریافت قیمت‌های هر سایز (مستقل از رنگ) =====
        size_prices = data.get('size_prices', {})
        
        # ===== به‌روزرسانی واریانت‌ها =====
        variant_updates = data.get('variant_updates', [])
        
        # ===== لیست برای نگهداری ID واریانت‌هایی که آپدیت شدن =====
        updated_variant_ids = []
        
        for update in variant_updates:
            color_name = update.get('color_name', '').strip()
            size_name = update.get('size_name', 'M')
            stock = update.get('stock', 0)
            price = size_prices.get(size_name, 0)  # قیمت از size_prices
            is_new = update.get('is_new', False)
            
            if not color_name:
                continue
            
            # پیدا کردن یا ایجاد رنگ
            color, _ = Color.objects.get_or_create(
                name=color_name,
                defaults={'code': '#cccccc'}
            )
            size, _ = Size.objects.get_or_create(name=size_name)
            
            # ===== اعمال تخفیف روی قیمت =====
            if discount_percent > 0 and price > 0:
                final_price = int(price * (100 - discount_percent) / 100)
            else:
                final_price = price
            
            if is_new:
                # ===== ایجاد واریانت جدید =====
                if stock > 0:
                    variant = ProductVariant.objects.create(
                        product=product,
                        color=color,
                        size=size,
                        stock=stock,
                        price=final_price
                    )
                    updated_variant_ids.append(variant.id)
            else:
                # ===== به‌روزرسانی واریانت موجود =====
                variant_id = update.get('id')
                if variant_id:
                    try:
                        variant = ProductVariant.objects.get(id=variant_id, product=product)
                        variant.stock = stock
                        variant.price = final_price  # ← قیمت از size_prices
                        variant.save()
                        updated_variant_ids.append(variant.id)
                    except ProductVariant.DoesNotExist:
                        # ===== اگه واریانت با ID پیدا نشد، ایجاد کن =====
                        if stock > 0:
                            variant = ProductVariant.objects.create(
                                product=product,
                                color=color,
                                size=size,
                                stock=stock,
                                price=final_price
                            )
                            updated_variant_ids.append(variant.id)
        
        # ===== برای واریانت‌های موجود که در لیست نبودن، قیمت‌شون رو هم آپدیت کن =====
        # این کار باعث میشه واریانت‌هایی که موجودی 0 دارن ولی توی لیست نیستن هم قیمت‌شون آپدیت بشه
        all_variants = product.variants.all()
        for variant in all_variants:
            if variant.id not in updated_variant_ids:
                # اگه واریانت توی لیست نبود، قیمت رو از size_prices بگیر
                size_name = variant.size.name
                price = size_prices.get(size_name, 0)
                if discount_percent > 0 and price > 0:
                    final_price = int(price * (100 - discount_percent) / 100)
                else:
                    final_price = price
                variant.price = final_price
                variant.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'محصول با موفقیت به‌روزرسانی شد',
            'product_id': product.id
        })
        
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'محصول یافت نشد'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# ===== DELETE PRODUCT =====
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def delete_product(request, product_id):
    """API حذف محصول (غیرفعال کردن برای فروشگاه)"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    try:
        product = Product.objects.get(id=product_id)
        
        # ===== غیرفعال کردن برای فروشگاه =====
        product.is_active = False
        product.is_available = False
        product.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'محصول با موفقیت از فروشگاه حذف شد'
        })
        
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'محصول یافت نشد'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
    
# ===== RESTORE PRODUCT =====
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def restore_product(request, product_id):
    """API بازیابی محصول"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    try:
        product = Product.objects.get(id=product_id)
        product.is_active = True
        product.is_available = True
        product.save()
        return JsonResponse({
            'status': 'success',
            'message': 'محصول با موفقیت بازیابی شد'
        })
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'محصول یافت نشد'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# ===== DELETE PERMANENT =====
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def delete_permanent(request, product_id):
    """API حذف کامل محصول (فقط اگه در سفارش نباشه)"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    try:
        product = Product.objects.get(id=product_id)
        
        # ===== چک کن در سفارش استفاده شده =====
        from orders.models import OrderItem
        has_orders = OrderItem.objects.filter(product_name__icontains=product.name).exists()
        
        if has_orders:
            return JsonResponse({
                'status': 'error',
                'message': 'این محصول در سفارشات استفاده شده است، قابل حذف کامل نیست'
            })
        
        # ===== حذف تصاویر =====
        for img in product.images.all():
            if img.image:
                img.image.delete(save=False)
            img.delete()
        
        # ===== حذف واریانت‌ها =====
        product.variants.all().delete()
        
        # ===== حذف مشخصات =====
        product.specifications.all().delete()
        
        # ===== حذف محصول =====
        product.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'محصول با موفقیت حذف شد'
        })
        
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'محصول یافت نشد'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
  
    
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def manage_products(request):
    """صفحه مدیریت محصولات آماده"""
    return render(request, 'tailor_panel/manage-readymade-products.html')