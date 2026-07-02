from django.urls import path
from . import views
urlpatterns = [
    path('list/' ,views.product_list , name='list'),
    path('product/<slug:product_slug>/' ,views.product_details , name='detail')
]