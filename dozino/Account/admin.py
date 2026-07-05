from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'full_name',
        'phone_number',
        'gender',
        'address',
        'postal_code',
        'is_active',
        'is_staff',
    )
    
    list_filter = (
        'gender',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    
    search_fields = (
        'username',
        'full_name',
        'phone_number',
        'address',
    )
    
    fieldsets = (
        ('اطلاعات ورود', {
            'fields': ('username', 'password')
        }),
        ('اطلاعات شخصی', {
            'fields': (
                'full_name',
                'phone_number',
                'gender',
                'address',
                'postal_code',
                'profile_image'
            )
        }),
        ('دسترسی‌ها', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        ('تاریخ‌ها', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'fields': (
                'username',
                'full_name',
                'phone_number',
                'gender',
                'address',
                'postal_code',
                'password1',
                'password2',
            )
        }),
    )