from django.urls import path
from . import views

urlpatterns =[
    path('register/', views.register , name='register'),
    path('login/', views.user_login , name='login'),
    path('profile/', views.profile , name='profile'),
    path('resetpassword/', views.resetpassword , name='resetpassword'),
    path('new_password/' , views.new_password , name='new_password' ),
    path('logout/' , views.user_logout , name='logout')
        
    ]