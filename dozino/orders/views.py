from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # محاسبه تعداد محصولات هر سفارش
    for order in user_orders:
        order.total_items = order.items.count()
    
    context = {
        'orders': user_orders
    }
    
    return render(request, 'orders/orders.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    
    return render(request, 'orders/order_detail.html', context)