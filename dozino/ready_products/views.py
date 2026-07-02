from django.shortcuts import render ,get_object_or_404
from .models import Product, ProductImage, ProductVariant, ProductSpecification

def product_list(request):
    products = Product.objects.all()
    
    for product in products:
        product.main_image = product.images.filter(is_main=True).first()
    
    context = {
        'products': products,
    }
    return render(request,'products/ready-made clothes/list.html',context)

def product_details(request,product_slug):
    product = get_object_or_404(Product, slug=product_slug) 
    
    images = product.images.all()
    
    variants = product.variants.all()
    
    specifications = product.specifications.all()
    
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'images': images,
        'variants': variants,
        'specifications': specifications,
        'related_products': related_products,
    }
    return render(request,'products/ready-made clothes/details.html',context)