from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def tailor_dashboard(request):
    return render(request, 'tailor_panel/dashboard.html')