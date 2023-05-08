from django.shortcuts import render

# Create your views here.

def dashboard_atlet_page(request):
    return render(request, 'dashboard_atlet_page.html')

def dashboard_pelatih_page(request):
    return render(request, 'dashboard_pelatih_page.html')

def dashboard_umpire_page(request):
    return render(request, 'dashboard_umpire_page.html')