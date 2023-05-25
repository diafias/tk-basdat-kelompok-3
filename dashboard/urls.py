from django.urls import path
from dashboard.views import create_ujian_kualifikasi, dashboard_atlet_page, dashboard_pelatih_page, dashboard_umpire_page, list_ujian_kualifikasi, tes_kualifikasi
from dashboard.views import pertanyaan_kualifikasi, list_atlet_pelatih, list_atlet_umpire, daftar_event, daftar_event2, pilih_kategori
from dashboard.views import read_list_event, hasil_pertandingan_page, quarterfinals_page, finals_page, third_place_page
from dashboard.views import semifinals_page, game_results_page, enrolled_event, enrolled_event_partai_kompetisi
from dashboard.views import daftar_sponsor_untuk_atlet, list_sponsor, list_atlet_create

app_name = 'dashboard'

urlpatterns = [
    path('atlet/', dashboard_atlet_page, name='dashboard_atlet_page'),
    path('pelatih/', dashboard_pelatih_page, name='dashboard_pelatih_page'),   
    path('umpire/', dashboard_umpire_page, name='dashboard_umpire_page'),
    path('tes_kualifikasi/', tes_kualifikasi, name='tes_kualifikasi'),
    path('pertanyaan_kualifikasi/', pertanyaan_kualifikasi, name='pertanyaan_kualifikasi'),
    path('list_atlet_pelatih/', list_atlet_pelatih, name='list_atlet_pelatih'),
    path('list_atlet_umpire/', list_atlet_umpire, name='list_atlet_umpire'),
    path('daftar_event/', daftar_event, name='daftar_event'),
    path('daftar_event2/', daftar_event2, name='daftar_event2'),
    path('pilih_kategori/', pilih_kategori, name='pilih_kategori'),
    path('enrolled_event/', enrolled_event, name='enrolled_event'),
    path('enrolled_event_partai_kompetisi/', enrolled_event_partai_kompetisi, name='enrolled_event_partai_kompetisi'),
    path('daftar_sponsor_untuk_atlet/', daftar_sponsor_untuk_atlet, name='daftar_sponsor_untuk_atlet'),
    path('list_sponsor/', list_sponsor, name='list_sponsor'),
    path('read_list_event/', read_list_event, name='read_list_event'),
    path('hasil_pertandingan_page/', hasil_pertandingan_page, name='hasil_pertandingan_page'),
    path('quarterfinals_page/', quarterfinals_page, name='quarterfinals_page'),
    path('finals_page/', finals_page, name='finals_page'),
    path('third_place_page/', third_place_page, name='third_place_page'),
    path('semifinals_page/', semifinals_page, name='semifinals_page'),
    path('game_results_page/', game_results_page, name='game_results_page'),
    path('list_atlet_create/', list_atlet_create, name='list_atlet_create'),
    path('list_ujian_kualifikasi/', list_ujian_kualifikasi, name='list_ujian_kualifikasi'),
    path('create_ujian_kualifikasi/', create_ujian_kualifikasi, name='create_ujian_kualifikasi'),
]