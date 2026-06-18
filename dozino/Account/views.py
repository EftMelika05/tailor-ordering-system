from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model

def register(request):
 if request.method=='POST':
  role=request.POST['role']
  
 return render(request ,'Account/register.html' )

def login(request):
 return render(request , 'Account/login.html')

def resetpass(request):
 return render(request , 'Account/reset.html')

def profile(request):
 return render(request , 'Account/profile.html')