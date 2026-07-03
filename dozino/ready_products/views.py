from django.shortcuts import render ,get_object_or_404
from .models import Category,Product, ProductImage, ProductVariant, ProductSpecification , Color ,Size
from django.core.paginator import Paginator
from django.db.models import Min, Q

def product_list(request):

    products = Product.objects.prefetch_related(
        "images",
        "variants",
        "category"
    ).all()

    search = request.GET.get("search")
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    categories = Category.objects.all()    
    category= request.GET.get("category")

    if category:
      products = products.filter(
        category__gender=category)

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
        "categories": categories,
        "selected_sort": sort or "",
    }

    return render(request,"products/ready-made clothes/list.html",context)

def product_details(request,product_slug):
    product = get_object_or_404(Product, slug=product_slug) 
    
    images = product.images.all()
    
    variants = product.variants.all()
    
    specifications = product.specifications.all()
    
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    colors = Color.objects.filter(productvariant__product=product).distinct()
    sizes = Size.objects.filter(
    productvariant__product=product).distinct()
    
    context = {
        'product': product,
        'images': images,
        'variants': variants,
        'specifications': specifications,
        'related_products': related_products,
        'sizes': sizes ,
        'colors':colors ,
    }
    return render(request,'products/ready-made clothes/details.html',context)