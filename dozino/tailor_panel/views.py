from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.db.models import Q
import json
import time
import base64

# ===== import از ready_products =====
from ready_products.models import Category, Product, Color, Size, ProductVariant, ProductImage, ProductSpecification

# ===== import از orders =====
from orders.models import Order, OrderItem


# ===== AUTH VIEWS =====
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



@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def dashboard(request):
    """پنل اصلی خیاط با لیست سفارشات"""
    all_orders = Order.objects.all().order_by('-created_at')
    
    # جستجو
    search = request.GET.get('search')
    if search:
        all_orders = all_orders.filter(id__icontains=search)
    
    # دسته‌بندی بر اساس وضعیت
    new_orders = all_orders.filter(status__in=['pending', 'paid'])
    prep_orders = all_orders.filter(status='processing')
    sent_orders = all_orders.filter(status='shipped')
    completed_orders = all_orders.filter(status='completed')
    cancelled_orders = all_orders.filter(status='cancelled')
    
    # محاسبه تعداد آیتم‌ها
    for order in all_orders:
        order.total_items = order.items.count()
    
    context = {
        'new_orders': new_orders,
        'prep_orders': prep_orders,
        'sent_orders': sent_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'all_orders': all_orders,
    }
    
    return render(request, 'tailor_panel/tailor_panel.html', context)


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
        
        # ===== اصلاح: نگاشت وضعیت‌ها =====
        # کلیدها همان مقداری هستن که از frontend میاد
        status_map = {
            'processing': 'processing',   # پذیرش → در حال پردازش
            'shipped': 'shipped',         # ارسال شده
            'cancelled': 'cancelled',     # لغو شده
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


# ===== PRODUCT REGISTRATION VIEWS =====
@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def register_product_page(request):
    """صفحه ثبت محصول آماده"""
    return render(request, 'tailor_panel/registering-products.html')


@login_required(login_url='tailor_panel:tailor_login')
@staff_member_required(login_url='tailor_panel:tailor_login')
def register_product_submit(request):
    """API ثبت محصول آماده"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})

    try:
        data = json.loads(request.body)
        
        category = Category.objects.get(id=data['category_id'])
        
        product_name = data.get('product_name', '').strip()
        if not product_name:
            return JsonResponse({
                'status': 'error',
                'message': 'نام محصول نمی‌تواند خالی باشد'
            })
        
        base_slug = slugify(product_name)
        if not base_slug:
            base_slug = 'product-' + str(int(time.time()))
        
        final_slug = base_slug
        counter = 1
        while Product.objects.filter(slug=final_slug).exists():
            final_slug = f"{base_slug}-{counter}"
            counter += 1
        
        product = Product.objects.create(
            category=category,
            name=product_name,
            slug=final_slug,
            price=0,
            description=data.get('description', ''),
            is_available=True,
            is_active=True,
        )

        # مشخصات فنی
        specs = data.get('specifications', {})
        for spec_name, spec_value in specs.items():
            if spec_value:
                ProductSpecification.objects.create(
                    product=product,
                    spec_name=spec_name,
                    spec_value=spec_value
                )

        # رنگ‌ها، سایزها و موجودی
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
                    price = size_prices.get(size_name, 0)

                    ProductVariant.objects.create(
                        product=product,
                        color=color,
                        size=size,
                        stock=stock,
                        price=price
                    )

        # تصاویر
        images_data = data.get('images', [])
        for i, image_data in enumerate(images_data):
            try:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                file_data = ContentFile(base64.b64decode(imgstr), name=f"{product.slug}_{i}.{ext}")
                
                ProductImage.objects.create(
                    product=product,
                    image=file_data,
                    is_main=(i == 0)
                )
            except Exception as e:
                print(f"⚠️ خطا در ذخیره تصویر {i}: {e}")

        return JsonResponse({
            'status': 'success',
            'message': 'محصول با موفقیت ثبت شد',
            'product_id': product.id,
            'product_slug': product.slug
        })

    except Category.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'دسته‌بندی انتخاب شده وجود ندارد'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })