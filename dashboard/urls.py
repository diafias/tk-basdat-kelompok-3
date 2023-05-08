from django.urls import path
from dashboard.views import dashboard_atlet_page
from dashboard.views import dashboard_pelatih_page
from dashboard.views import dashboard_umpire_page
from dashboard.views import tes_kualifikasi
from dashboard.views import pertanyaan_kualifikasi
from dashboard.views import daftar_atlet
from dashboard.views import list_atlet
from dashboard.views import daftar_event
from dashboard.views import daftar_event2
from dashboard.views import pilih_kategori
from dashboard.views import enrolled_event

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_atlet_page, name='dashboard_atlet_page'),
    path('dashboard_pelatih_page/', dashboard_pelatih_page, name='dashboard_pelatih_page'),   
    path('dashboard_umpire_page/', dashboard_umpire_page, name='dashboard_umpire_page'),
    path('tes_kualifikasi/', tes_kualifikasi, name='tes_kualifikasi'),
    path('pertanyaan_kualifikasi/', pertanyaan_kualifikasi, name='pertanyaan_kualifikasi'),
    path('daftar_atlet/', daftar_atlet, name='daftar_atlet'),
    path('list_atlet/', list_atlet, name='list_atlet'),
    path('daftar_event/', daftar_event, name='daftar_event'),
    path('daftar_event2/', daftar_event2, name='daftar_event2'),
    path('pilih_kategori/', pilih_kategori, name='pilih_kategori'),
    path('enrolled_event/', enrolled_event, name='enrolled_event'),
]
