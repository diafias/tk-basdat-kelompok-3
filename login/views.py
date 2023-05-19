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
            if request.session['role'] == 'atlet':
                return redirect('/atlet')
            elif request.session['role'] == 'pelatih':
                return redirect('/pelatih')
            elif request.session['role'] == 'umpire':
                return redirect('/umpire')
    return render(request, 'login_page.html')

def logout(request):
    request.session.flush()
    return redirect('/')

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
        if get_query("SELECT id FROM ATLET WHERE id = '{id_member}'".format(id_member = request.session['user_id'])) != []:
            request.session['role'] = 'atlet'
        elif get_query("SELECT id FROM PELATIH WHERE id = '{id_member}'".format(id_member = request.session['user_id'])) != []:
            request.session['role'] = 'pelatih'
        elif get_query("SELECT id FROM UMPIRE WHERE id = '{id_member}'".format(id_member = request.session['user_id'])) != []:
            request.session['role'] = 'umpire'
        return True
    
