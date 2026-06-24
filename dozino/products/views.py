from  django.shortcuts import render

def ready_mades_list(request):
    return render(request,'products/ready-made clothes/list.html')

def ready_mades_details(request):
    return render(request ,'products/ready-made clothes/details.html' )