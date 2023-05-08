from django.urls import path
from login.views import pilih_role
from login.views import show_daftar_akun_atlet
from login.views import show_daftar_akun_pelatih
from login.views import show_daftar_akun_umpire
from login.views import landing_page
from login.views import login_page


app_name = 'login'

urlpatterns = [
    path('landing_page/', landing_page, name='landing_page'),
    path("pilih_role/", pilih_role, name='pilih_role'),
    path('daftar_akun_atlet/', show_daftar_akun_atlet, name='daftar_akun_atlet'),
    path('daftar_akun_pelatih/', show_daftar_akun_pelatih, name='daftar_akun_pelatih'),
    path('daftar_akun_umpire/', show_daftar_akun_umpire, name='daftar_akun_umpire'),
    path('login_page/', login_page, name='login_page'),
    
]
