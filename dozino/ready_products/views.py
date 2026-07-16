import json
import time
import base64
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.files.base import ContentFile

from .models import Category, Product, Color, Size, ProductVariant, ProductImage, ProductSpecification


def product_list(request):
    # ===== فقط محصولات فعال =====
    products = Product.objects.prefetch_related("images", "variants", "category").filter(
        is_active=True,
        is_available=True
    )
    
    for product in products:
        if not product.slug:
            product.slug = slugify(product.name)
            product.save()
            
    search = request.GET.get("search")
    if search:
        products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))

    category_slug = request.GET.get("category")
    if category_slug and category_slug != "all":
        products = products.filter(category__slug=category_slug)

    sort = request.GET.get("sort")
    if sort == "cheap":
        products = products.order_by("price")
    elif sort == "expensive":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-id")
    elif sort == "oldest":
        products = products.order_by("id")
    else:
        products = products.order_by("-id")

    for product in products:
        product.main_image = product.images.filter(is_main=True).first()
        if not product.main_image:
            product.main_image = product.images.first()
        product.available = product.variants.filter(stock__gt=0).exists()
        
        # ===== وضعیت موجودی =====
        if product.available:
            product.stock_status = "موجود"
            product.stock_status_class = "in-stock"
        else:
            product.stock_status = "ناموجود"
            product.stock_status_class = "out-of-stock"
            
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "search": search or "",
        "selected_category": category_slug or "all",
        "selected_sort": sort or "",
    }

    return render(request, "products/ready-made clothes/list.html", context)


def product_details(request, product_slug):
    # ===== فقط محصولات فعال =====
    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    
    images = product.images.all()
    variants = product.variants.all()
    specifications = product.specifications.all()
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    colors = Color.objects.filter(productvariant__product=product).distinct()
    sizes = Size.objects.filter(productvariant__product=product).distinct()
    
    # ===== قیمت‌ها برای هر سایز با تخفیف =====
    unique_sizes = []
    seen = set()
    discount_percent = product.discount_percent or 0
    
    for variant in variants:
        if variant.size.name not in seen:
            seen.add(variant.size.name)
            
            # قیمت با تخفیف (همون قیمت واریانت)
            current_price = variant.price
            
            # ===== قیمت اصلی (قبل از تخفیف) =====
            if discount_percent > 0 and current_price:
                original_price = int(current_price / (1 - discount_percent / 100))
            else:
                original_price = current_price
            
            unique_sizes.append({
                'name': variant.size.name,
                'price': current_price,
                'original_price': original_price  # ← قیمت اصلی برای نمایش
            })
    
    # ===== قیمت پیش‌فرض (سایز M یا اولین سایز) =====
    default_price = 0
    default_original_price = 0
    
    if variants.exists():
        # اول سایز M رو پیدا کن
        for variant in variants:
            if variant.size.name == 'M':
                default_price = variant.price
                if discount_percent > 0 and default_price:
                    default_original_price = int(default_price / (1 - discount_percent / 100))
                else:
                    default_original_price = default_price
                break
        
        # اگه سایز M نبود، اولین سایز رو بگیر
        if not default_price:
            default_price = variants.first().price
            if discount_percent > 0 and default_price:
                default_original_price = int(default_price / (1 - discount_percent / 100))
            else:
                default_original_price = default_price

    context = {
        'product': product,
        'images': images,
        'variants': variants,
        'specifications': specifications,
        'related_products': related_products,
        'sizes': sizes,
        'colors': colors,
        'default_price': default_price,
        'default_original_price': default_original_price,  # ← قیمت اصلی پیش‌فرض
        'unique_sizes': unique_sizes,
        'discount_percent': discount_percent,
    }
    return render(request, 'products/ready-made clothes/details.html', context)