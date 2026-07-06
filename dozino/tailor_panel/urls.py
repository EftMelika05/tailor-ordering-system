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
    
    # ===== PRODUCT REGISTRATION =====
    path('products/register/', views.register_product_page, name='register_product'),
    path('products/register/submit/', views.register_product_submit, name='register_product_submit'),
]