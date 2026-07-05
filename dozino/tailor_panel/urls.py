from django.urls import path
from . import views

app_name = 'tailor_panel'

urlpatterns = [
    path('tailor-login/', views.tailor_login, name='tailor_login'),
    path('dashboard/', views.dashboard, name='dashboard'),   

]