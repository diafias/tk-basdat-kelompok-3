from django.shortcuts import redirect, render
from project_django.utils import get_query, insert_row

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
    #Read
    id_user = request.session['user_id']
    enrolled_event = get_query("""
    SELECT e.nama_event, e.tahun, e.nama_stadium, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai
    FROM ATLET a
    JOIN ATLET_KUALIFIKASI ak ON a.id = ak.id_atlet
    LEFT JOIN ATLET_GANDA ag ON ak.id_atlet = ag.id_atlet_kualifikasi OR ak.id_atlet = ag.id_atlet_kualifikasi_2
    JOIN PESERTA_KOMPETISI pk ON ak.id_atlet = pk.id_atlet_kualifikasi OR ag.id_atlet_ganda = pk.id_atlet_ganda
    JOIN PESERTA_MENDAFTAR_EVENT pme ON pk.nomor_peserta = pme.nomor_peserta
    JOIN EVENT e ON pme.nama_event = e.nama_event AND pme.tahun = e.tahun
    WHERE a.id = '{id_atlet}'
    """.format(id_atlet = id_user))

    context = {
        'enrolled_event_list': enrolled_event,   
    }

    return render(request, 'enrolled_event.html', context)

def enrolled_event_partai_kompetisi(request):
    id_user = request.session['user_id']
    enrolled_partai = get_query("""
    SELECT ppk.nama_event, ppk.tahun_event, ppk.jenis_partai, e.nama_stadium, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai
    FROM ATLET a
    JOIN ATLET_KUALIFIKASI ak ON a.id = ak.id_atlet
    LEFT JOIN ATLET_GANDA ag ON ak.id_atlet = ag.id_atlet_kualifikasi OR ak.id_atlet = ag.id_atlet_kualifikasi_2
    JOIN PESERTA_KOMPETISI pk ON ak.id_atlet = pk.id_atlet_kualifikasi OR ag.id_atlet_ganda = pk.id_atlet_ganda
    JOIN PARTAI_PESERTA_KOMPETISI ppk ON pk.nomor_peserta = ppk.nomor_peserta
    JOIN EVENT e ON ppk.nama_event = e.nama_event AND ppk.tahun_event = e.tahun
    WHERE a.id = '{id_atlet}'
    """.format(id_atlet = id_user))

    context = {
        'enrolled_partai_list': enrolled_partai,   
    }
    return render(request, 'enrolled_event_partai_kompetisi.html', context)

def daftar_sponsor_untuk_atlet(request):
    id_user = request.session['user_id']

    if request.method == "post":
        nama_brand = request.POST.get('nama_brand')
        tgl_mulai = request.POST.get('start_date')
        tgl_selesai = request.POST.get('end_date')

        id_sponsor = get_query("""
        SELECT id FROM SPONSOR WHERE nama_brand = '{brand}'
        """.format(brand = nama_brand))

        insert_row("""
        INSERT INTO ATLET_SPONSOR (id_atlet, id_sponsor, tgl_mulai, tgl_selesai) VALUES ('{id_atlet}', '{sponsor}', '{start}', '{end}')
        """.format(id_atlet = id_user, sponsor= id_sponsor[0].id, start = tgl_mulai, end = tgl_selesai))

        return redirect('/list_sponsor')

    list_sponsor = get_query("""
    SELECT nama_brand FROM SPONSOR
    """)

    context = {
        'list_sponsor': list_sponsor,
    }
    return render(request, 'daftar_sponsor_untuk_atlet.html', context)

def list_sponsor(request):
    id_user = request.session['user_id']
    sponsor = get_query("""
    SELECT DISTINCT s.nama_brand, sa.tgl_mulai, sa.tgl_selesai 
    FROM SPONSOR s, ATLET_SPONSOR sa, ATLET a 
    WHERE s.id = sa.id_sponsor AND sa.id_atlet = '{id_atlet}'
    """.format(id_atlet = id_user)) 

    context = {
        'sponsor_list': sponsor  
    }

    return render(request, 'list_sponsor.html', context)

def is_authenticated(request):
    try:
        request.session['user']
        return True
    except KeyError:
        return False