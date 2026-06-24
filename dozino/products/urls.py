from django.urls import path
from . import views

urlpatterns=[
    path('list/' , views.ready_mades_list , name='list'),
    path('details/' , views.ready_mades_details , name='details')
]