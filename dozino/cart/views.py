from django.shortcuts import render
from .views import *
# Create your views here.
def cart(request):
    return render(request, 'cart/cart.html')
