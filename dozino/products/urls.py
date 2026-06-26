from django.urls import path
from . import views

urlpatterns=[
    path('list/' , views.ready_mades_list , name='list'),
    path('details/' , views.ready_mades_details , name='details'),
    path('T_shirt/' , views.design_T_shirt , name='T_shirt' ),
    path('Dors/' , views.design_dors , name='dors'),
    path('Trousers/' , views.design_trousers , name='trousers')
]