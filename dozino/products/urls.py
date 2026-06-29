from django.urls import path

from products.views import (
    design_T_shirt,
    calculate_tshirt,
    ready_mades_list,
    design_trousers,
    calculate_trousers,
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
    "dors/",
    design_dors,
    name="design_dors"
    ),
    
    
    path(
    "dors/calculate/",
    calculate_dors,
    name="calculate_dors"
    ),

    path(
    "trousers/",
    design_trousers,
    name="trousers"
    ),

    path(
    "trousers/calculate/",
    calculate_trousers,
    name="calculate_trousers"   
    ),


]