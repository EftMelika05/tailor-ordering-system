from django.urls import path

from products.views import (
    design_T_shirt,
    calculate_tshirt,
    ready_mades_list,
    trousers,
    design_dors,
    calculate_dors,
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
    
    path(
    'trousers/',
    trousers,
    name='trousers'
    ),
    
    path(
    "dors/",
    design_dors,
    name="design_dors"
    ),
    
    
    path(
    "dors/calculate/",
    calculate_dors,
    name="calculate_dors"
    ),

]