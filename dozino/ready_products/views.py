from django.shortcuts import render

def list(request):
    return render(request,'products/ready-made clothes/list.html')
def details(request):
    return render(request,'products/ready-made clothes/details.html')
