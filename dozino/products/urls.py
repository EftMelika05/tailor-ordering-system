from django.urls import path

from products.views import (
    design_T_shirt,
    calculate_tshirt,
    ready_mades_list,
)

urlpatterns = [

    path(
        'T_shirt/',
        design_T_shirt,
        name='T_shirt'
    ),

    path(
        'T_shirt/calculate/',
        calculate_tshirt,
        name='calculate_tshirt'
    ),
    
    path('list/' ,ready_mades_list , name='list'),


]