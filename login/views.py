from django.shortcuts import redirect, render
from project_django.utils import get_query
import re
from django.contrib import messages


# Create your views here.
def pilih_role(request):
    return render(request, 'pilih_role.html')

def show_daftar_akun_atlet(request):
    if request.method == "POST":
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        tinggi_badan = request.POST.get('tinggi_badan')
        play = request.POST.get('play')
        jenis_kelamin = request.POST.get('jenis_kelamin')

        if nama == "" or email == "" or negara == "" or tanggal_lahir == "" or tinggi_badan == "" or play == "" or jenis_kelamin == "":
            messages.error(request, 'Please fill all the fields' )
            return redirect('/daftar_akun_atlet')
            
        insert_member = get_query("""
        INSERT INTO MEMBER (nama, email)
        VALUES ('{nama_member}', '{email_member}')
        """.format(nama_member = nama, email_member = email))

        is_error = re.search("^Email already exists", str(insert_member[0]))
        if is_error:
            messages.error(request, 'Email already exists' )
            return redirect('/daftar_akun_atlet')

        id_member = get_query("""
        SELECT id FROM MEMBER
        WHERE nama = '{nama_member}' AND email = '{email_member}'
        """.format(nama_member = nama, email_member = email))[0].id

        get_query("""
        INSERT INTO ATLET (id, tgl_lahir, negara_asal, play_right, height, jenis_kelamin)
        VALUES ('{id_member}', '{tanggal_lahir_member}', '{negara_member}', {play_member}, {tinggi_badan_member}, {jenis_kelamin_member})
        """.format(id_member = id_member, tanggal_lahir_member = tanggal_lahir, negara_member = negara, play_member = play, tinggi_badan_member = tinggi_badan, jenis_kelamin_member = jenis_kelamin))

        return redirect('/login_page')
        
    return render(request, 'daftar_akun_atlet.html')

def show_daftar_akun_pelatih(request):
    if request.method == "POST":
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        tanggal_mulai = request.POST.get('tanggal_mulai')
        spesialisasi = request.POST.getlist('spesialisasi')

        if nama == "" or email == "" or negara == "" or tanggal_mulai == "" or spesialisasi == []:
            messages.error(request, 'Please fill all the fields' )
            return redirect('/daftar_akun_pelatih')

        insert_member = get_query("""
        INSERT INTO MEMBER (nama, email)
        VALUES ('{nama_member}', '{email_member}')
        """.format(nama_member = nama, email_member = email))

        is_error = re.search("^Email already exists", str(insert_member[0]))
        if is_error:
            messages.error(request, 'Email already exists' )
            return redirect('/daftar_akun_pelatih')

        id_member = get_query("""
        SELECT id FROM MEMBER
        WHERE nama = '{nama_member}' AND email = '{email_member}'
        """.format(nama_member = nama, email_member = email))[0].id

        get_query("""
        INSERT INTO PELATIH (id, tanggal_mulai)
        VALUES ('{id_member}', '{tanggal_mulai_member}')
        """.format(id_member = id_member, tanggal_mulai_member = tanggal_mulai))

        for spesialisasi_pelatih in spesialisasi:
            id_spesialiasi = get_query("""
            SELECT id FROM SPESIALISASI 
            WHERE spesialisasi = '{nama_spesialisasi}'
            """.format(nama_spesialisasi = spesialisasi_pelatih))[0].id

            get_query("""
            INSERT INTO PELATIH_SPESIALISASI (id_pelatih, id_spesialisasi)
            VALUES ('{id_pelatih_member}', '{id_spesialisasi_pelatih}')
            """.format(id_pelatih_member = id_member, id_spesialisasi_pelatih = id_spesialiasi))
        
        return redirect('/login_page')

    return render(request, 'daftar_akun_pelatih.html')

def show_daftar_akun_umpire(request):
    if request.method == "POST":
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')

        if nama == "" or email == "" or negara == "":
            messages.error(request, 'Please fill all the fields' )
            return redirect('/daftar_akun_umpire')
        
        insert_member = get_query("""
        INSERT INTO MEMBER (nama, email)
        VALUES ('{nama_member}', '{email_member}')
        """.format(nama_member = nama, email_member = email))

        is_error = re.search("^Email already exists", str(insert_member[0]))
        if is_error:
            messages.error(request, 'Email already exists' )
            return redirect('/daftar_akun_umpire')

        id_member = get_query("""
        SELECT id FROM MEMBER 
        WHERE nama = '{nama_member}' AND email = '{email_member}'
        """.format(nama_member = nama, email_member = email))[0].id
        
        get_query("""
        INSERT INTO UMPIRE (id, negara)
        VALUES ('{id_member}', '{negara_member}')
        """.format(id_member = id_member, negara_member = negara))

        return redirect('/login_page')

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
