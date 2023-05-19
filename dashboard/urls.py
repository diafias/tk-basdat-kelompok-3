from django.urls import path
from dashboard.views import dashboard_atlet_page, dashboard_pelatih_page, dashboard_umpire_page, tes_kualifikasi
from dashboard.views import pertanyaan_kualifikasi, daftar_atlet, list_atlet, daftar_event, daftar_event2, pilih_kategori
from dashboard.views import read_list_event, hasil_pertandingan_page, quarterfinals_page, finals_page, third_place_page
from dashboard.views import semifinals_page, game_results_page, enrolled_event, enrolled_event_partai_kompetisi
from dashboard.views import daftar_sponsor_untuk_atlet, list_sponsor

app_name = 'dashboard'

urlpatterns = [
    path('atlet/', dashboard_atlet_page, name='dashboard_atlet_page'),
    path('pelatih/', dashboard_pelatih_page, name='dashboard_pelatih_page'),   
    path('umpire/', dashboard_umpire_page, name='dashboard_umpire_page'),
    path('tes_kualifikasi/', tes_kualifikasi, name='tes_kualifikasi'),
    path('pertanyaan_kualifikasi/', pertanyaan_kualifikasi, name='pertanyaan_kualifikasi'),
    path('daftar_atlet/', daftar_atlet, name='daftar_atlet'),
    path('list_atlet/', list_atlet, name='list_atlet'),
    path('daftar_event/', daftar_event, name='daftar_event'),
    path('daftar_event2/', daftar_event2, name='daftar_event2'),
    path('pilih_kategori/', pilih_kategori, name='pilih_kategori'),
    path('enrolled_event/', enrolled_event, name='enrolled_event'),
    path('enrolled_event_partai_kompetisi/', enrolled_event_partai_kompetisi, name='enrolled_event_partai_kompetisi'),
    path('daftar_sponsor_untuk_atlet/', daftar_sponsor_untuk_atlet, name='daftar_sponsor_untuk_atlet'),
    path('list_sponsor/', list_sponsor, name='list_sponsor'),
    path('list_event/', read_list_event, name='list_event'),
    path('hasil_pertandingan_page/', hasil_pertandingan_page, name='hasil_pertandingan_page'),
    path('quarterfinals_page/', quarterfinals_page, name='quarterfinals_page'),
    path('finals_page/', finals_page, name='finals_page'),
    path('third_place_page/', third_place_page, name='third_place_page'),
    path('semifinals_page/', semifinals_page, name='semifinals_page'),
    path('game_results_page/', game_results_page, name='game_results_page'),
]
