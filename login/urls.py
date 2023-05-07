from django.urls import path
from login.views import pilih_role
from login.views import show_daftar_akun_atlit
from login.views import show_daftar_akun_pelatih
from login.views import show_daftar_akun_umpire
from login.views import landing_page
from login.views import login_page


app_name = 'login'

urlpatterns = [
    #path('', pilih_role, name='pilih_role'),
    #path('', show_daftar_akun_atlit, name='daftar_akun_atlit'),
    #path('', show_daftar_akun_pelatih, name='daftar_akun_pelatih'),
    #path('', show_daftar_akun_umpire, name='daftar_akun_umpire'),
    #path('', landing_page, name='landing_page'),
    path('', login_page, name='login_page'),
    
]
