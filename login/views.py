from django.shortcuts import render

# Create your views here.
def pilih_role(request):
    return render(request, 'pilih_role.html')

def show_daftar_akun_atlet(request):
    return render(request, 'daftar_akun_atlet.html')

def show_daftar_akun_pelatih(request):
    return render(request, 'daftar_akun_pelatih.html')

def show_daftar_akun_umpire(request):
    return render(request, 'daftar_akun_umpire.html')

def landing_page(request):
    return render(request, 'landing_page.html')

def login_page(request):
    return render(request, 'login_page.html')