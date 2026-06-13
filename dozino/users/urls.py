from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('profile/',views.profile_view , name='profile'),
    path('login/',views.login , name='login'),
    path('register/',views.register , name='register'),
    path('reset/',auth_views.PasswordResetView.as_view(template_name='users/reset.html') , name='password_reset')
]