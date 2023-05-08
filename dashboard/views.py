from django.shortcuts import render

# Create your views here.

def dashboard_atlet_page(request):
    return render(request, 'dashboard_atlet_page.html')

def dashboard_pelatih_page(request):
    return render(request, 'dashboard_pelatih_page.html')

def dashboard_umpire_page(request):
    return render(request, 'dashboard_umpire_page.html')

def tes_kualifikasi(request):
    return render(request, 'tes_kualifikasi.html')

def pertanyaan_kualifikasi(request):
    return render(request, 'pertanyaan_kualifikasi.html')

def daftar_atlet(request):
    return render(request, 'daftar_atlet.html')

def list_atlet(request):
    return render(request, 'list_atlet.html')

def daftar_event(request):
    return render(request, 'daftar_event.html')

def daftar_event2(request):
    return render(request, 'daftar_event2.html')

def pilih_kategori(request):
    return render(request, 'pilih_kategori.html')

def enrolled_event(request):
    return render(request, 'enrolled_event.html')