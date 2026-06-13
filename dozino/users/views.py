from django.shortcuts import render

# Create your views here.
def register(request):
    return render(request, 'users/register.html')
def login(request):
    return render(request, 'users/login.html')
# def reset(request):
#     return render(request, 'users/reset.html')