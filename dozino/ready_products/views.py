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
    products = Product.objects.prefetch_related("images", "variants", "category").all()
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
    product = get_object_or_404(Product, slug=product_slug)
    images = product.images.all()
    variants = product.variants.all()
    specifications = product.specifications.all()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    colors = Color.objects.filter(productvariant__product=product).distinct()
    sizes = Size.objects.filter(productvariant__product=product).distinct()
    
    unique_sizes = []
    seen = set()
    for variant in variants:
        if variant.size.name not in seen:
            seen.add(variant.size.name)
            unique_sizes.append({
                'name': variant.size.name,
                'price': variant.price
            })
    
    default_price = 0
    if variants.exists():
        for variant in variants:
            if variant.size.name == 'M':
                default_price = variant.price
                break
        if not default_price:
            default_price = variants.first().price

    context = {
        'product': product,
        'images': images,
        'variants': variants,
        'specifications': specifications,
        'related_products': related_products,
        'sizes': sizes,
        'colors': colors,
        'default_price': default_price,
        'unique_sizes': unique_sizes,
    }
    return render(request, 'products/ready-made clothes/details.html', context)

