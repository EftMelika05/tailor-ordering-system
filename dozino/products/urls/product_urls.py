from django.urls import path

from products.views.product_views import product_list


urlpatterns = [
    path("", product_list),
]