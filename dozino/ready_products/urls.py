from django.urls import path
from . import views
urlpatterns = [
    path('list/', views.product_list, name='list'),
    path('product/<slug:product_slug>/', views.product_details, name='detail'),
    path('register/', views.register_product_page, name='register_product'),
    path('register/submit/', views.register_product_submit, name='register_product_submit'),
]