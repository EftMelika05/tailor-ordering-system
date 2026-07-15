from django.urls import path
from . import views

app_name = 'tailor_panel'

urlpatterns = [
    # ===== AUTH =====
    path('login/', views.tailor_login, name='tailor_login'),
    path('logout/', views.tailor_logout, name='tailor_logout'),
    
    # ===== DASHBOARD =====
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ===== ORDERS =====
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/update-status/', views.update_order_status, name='update_order_status'),
    
    # ===== PRODUCT REGISTRATION (محصولات آماده) =====
    path('products/register/', views.register_product_page, name='register_product'),
    path('products/register/submit/', views.register_product_submit, name='register_product_submit'),
    
    # ===== CUSTOM PRODUCT MANAGEMENT (مدیریت قیمت‌ها) =====
    path('custom-products/manage/', views.manage_custom_products, name='manage_custom_products'),
    
    # Fabric (فقط ویرایش قیمت)
    path('custom-products/fabric/edit/<int:fabric_id>/', views.edit_fabric, name='edit_fabric'),
    
    # Sticker (افزودن + حذف + ویرایش قیمت)
    path('custom-products/sticker/add/', views.add_sticker, name='add_sticker'),
    path('custom-products/sticker/update/<int:sticker_id>/', views.update_sticker, name='update_sticker'),
    path('custom-products/sticker/delete/<int:sticker_id>/', views.delete_sticker, name='delete_sticker'),
    
    # Options (فقط ویرایش قیمت)
    path('custom-products/option/update/<str:option_type>/<int:option_id>/', views.update_option_price, name='update_option_price'),
    
    # Site Prices
    path('custom-products/site-price/update/', views.update_site_prices, name='update_site_prices'),

    # ===== PRODUCT MANAGEMENT (مدیریت محصولات آماده) =====
    path('products/list/api/', views.get_products_list, name='get_products_list'),
    path('products/update/api/', views.update_product, name='update_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('products/restore/<int:product_id>/', views.restore_product, name='restore_product'),
    path('products/delete-permanent/<int:product_id>/', views.delete_permanent, name='delete_permanent'),
    path('manage-products/', views.manage_products, name='manage_products'),
]