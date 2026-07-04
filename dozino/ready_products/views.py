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


@staff_member_required
def register_product_page(request):
    return render(request, 'products/ready-made clothes/registering-products.html')


@staff_member_required
def register_product_submit(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})

    try:
        data = json.loads(request.body)
        
        print("\n" + "="*60)
        print("📦 داده دریافتی:")
        print(f"  category_id: {data.get('category_id')}")
        print(f"  product_name: {data.get('product_name')}")
        print(f"  images count: {len(data.get('images', []))}")
        print("="*60 + "\n")
        
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
        
        print(f"✅ محصول ایجاد شد: {product.name} - slug: {product.slug}")

        specs = data.get('specifications', {})
        for spec_name, spec_value in specs.items():
            if spec_value:
                ProductSpecification.objects.create(
                    product=product,
                    spec_name=spec_name,
                    spec_value=spec_value
                )

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
                print(f"✅ تصویر {i+1} ذخیره شد")
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