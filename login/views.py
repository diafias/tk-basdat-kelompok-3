from django.shortcuts import redirect, render
from project_django.utils import get_query

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
    if request.method == "POST":
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        result = authenticate(request, nama, email)
        if result:
            return redirect('/')
    return render(request, 'login_page.html')

def daftar_sponsor_untuk_atlet(request):
    return render(request, 'daftar_sponsor_untuk_atlet.html')

def read_list_event(request):
    return render(request, 'read_list_event.html')

def quarterfinals_page(request):
    return render(request,'matches_page/quarterfinals_page.html')

def finals_page(request):
    return render(request,'matches_page/finals_page.html')

def third_place_page(request):
    return render(request,'matches_page/third_place_page.html')

def semifinals_page(request):
    return render(request,'matches_page/semifinals_page.html')

def game_results_page(request):
    return render(request, 'game_results_page.html')

def hasil_pertandingan_page(request):
    return render(request, 'hasil_pertandingan_page.html')

def logout(request):
    request.session.flush()
    return redirect('/landing_page')

def authenticate(request, nama, email):
    data = get_query("""
    SELECT *
    FROM MEMBER
    WHERE nama = '{nama_member}' AND email = '{email_member}'
    """.format(nama_member = nama, email_member = email))
    
    if data == []:
        print("USER NOT FOUND")
        return False
    else:
        print("USER FOUND")
        request.session['user_id'] = str(data[0].id)
        return True