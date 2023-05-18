from django.urls import path
from login.views import pilih_role
from login.views import show_daftar_akun_atlet
from login.views import show_daftar_akun_pelatih
from login.views import show_daftar_akun_umpire
from login.views import landing_page
from login.views import login_page
from login.views import daftar_sponsor_untuk_atlet
from login.views import read_list_event
from login.views import quarterfinals_page
from login.views import finals_page
from login.views import third_place_page
from login.views import semifinals_page
from login.views import game_results_page
from login.views import hasil_pertandingan_page
from login.views import logout
app_name = 'login'

urlpatterns = [
    path('landing_page/', landing_page, name='landing_page'),
    path("pilih_role/", pilih_role, name='pilih_role'),
    path('daftar_akun_atlet/', show_daftar_akun_atlet, name='daftar_akun_atlet'),
    path('daftar_akun_pelatih/', show_daftar_akun_pelatih, name='daftar_akun_pelatih'),
    path('daftar_akun_umpire/', show_daftar_akun_umpire, name='daftar_akun_umpire'),
    path('login_page/', login_page, name='login_page'),
    path('read_list_event/', read_list_event, name='read_list_event'),
    path('quarterfinals_page/', quarterfinals_page, name='quarterfinals_page'),
    path('finals_page/', finals_page, name='finals_page'),
    path('third_place_page/', third_place_page, name='third_place_page'),
    path('semifinals_page/', semifinals_page, name='semifinals_page'),
    path('game_results_page/', game_results_page, name='game_results_page'),
    path('hasil_pertandingan_page/', hasil_pertandingan_page, name='hasil_pertandingan_page'),
    path('logout/', logout, name='logout'),
]
