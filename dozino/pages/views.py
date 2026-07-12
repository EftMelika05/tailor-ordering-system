from django.shortcuts import render
from django.contrib import messages
from ready_products.models import Product

def index(request):
  latest_products = Product.objects.all().order_by('-created_at')[:4]
  for product in latest_products:
    product.main_image = product.images.filter(is_main=True).first()
    if not product.main_image:
      product.main_image = product.images.first()
  context = {'latest_products': latest_products,}
  return render(request, 'pages/index.html',context)