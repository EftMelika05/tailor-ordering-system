from django.urls import path
from . import views

urlpatterns = [
    # path('login/',views.login_view , name='login'),
    path('register/',views.register , name='register')
    # path('reset/',views.reset_view , name='reset'),
    # path('profile/',views.profile_view , name='profile')
]