from  django.shortcuts import render

def ready_mades_list(request):
    return render(request,'products/ready-made clothes/list.html')

def ready_mades_details(request):
    return render(request ,'products/ready-made clothes/details.html' )

def design_T_shirt(request):
    return render(request,'products/custom clothes/T_shirt.html')

def design_dors(request):
    return render(request,'products/custom clothes/dors.html')

def design_trousers(request):
    return render(request,'products/custom clothes/trousers.html')