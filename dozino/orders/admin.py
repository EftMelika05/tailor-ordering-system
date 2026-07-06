from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_type', 'quantity', 'final_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'full_name', 'phone', 'address')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'status', 'total_price')
        }),
        ('اطلاعات ارسال', {
            'fields': ('full_name', 'phone', 'address', 'postal_code')
        }),
        ('تاریخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'product_type', 'quantity', 'final_price')
    list_filter = ('product_type',)
    search_fields = ('product_name',)