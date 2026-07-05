from django.urls import path
from . import views

app_name = 'tailor_panel'

urlpatterns = [
    path('', views.tailor_dashboard, name='dashboard'),
]