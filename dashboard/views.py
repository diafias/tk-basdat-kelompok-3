from django.shortcuts import render
from project_django.utils import get_query
import psycopg2

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
    enrolled_event = get_query("""
    SELECT DISTINCT e.nama_event, e.tahun, e.nama_stadium, e.total_hadiah, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai
    FROM EVENT e, PESERTA_MENDAFTAR_EVENT pme, PESERTA_KOMPETISI ptk, ATLET_GANDA ag, ATLET_KUALIFIKASI ak
    WHERE (e.nama_event, e.tahun) = (pme.nama_event, pme.tahun)
    AND pme.nomor_peserta = ptk.nomor_peserta
    AND (ptk.id_atlet_kualifikasi = ak.id_atlet OR (ptk.id_atlet_ganda = ag.id_atlet_ganda AND (ag.id_atlet_kualifikasi = ak.id_atlet) OR (ag.id_atlet_kualifikasi_2 = ak.id_atlet)))
    """) # NANTI GANTI ak.id_atlet JADI logged_in_user.id

    context = {
        'enrolled_event_list': enrolled_event,   
    }

    return render(request, 'enrolled_event.html', context)

def enrolled_event_partai_kompetisi(request):
    enrolled_partai = get_query("""
    SELECT DISTINCT pk.nama_event, pk.tahun_event, pk.jenis_partai, e.nama_stadium, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai
    FROM PARTAI_KOMPETISI pk, EVENT e, PARTAI_PESERTA_KOMPETISI ppk, PESERTA_KOMPETISI ptk, ATLET_GANDA ag, ATLET_KUALIFIKASI ak
    WHERE (pk.nama_event, pk.tahun_event) = (e.nama_event, e.tahun) 
    AND ppk.nomor_peserta = ptk.nomor_peserta 
    AND (ptk.id_atlet_kualifikasi = ak.id_atlet OR (ptk.id_atlet_ganda = ag.id_atlet_ganda AND (ag.id_atlet_kualifikasi = ak.id_atlet) OR (ag.id_atlet_kualifikasi_2 = ak.id_atlet)))
    """) # NANTI GANTI ak.id_atlet JADI logged_in_user.id

    context = {
        'enrolled_partai_list': enrolled_partai,   
    }
    return render(request, 'enrolled_event_partai_kompetisi.html', context)

def daftar_sponsor_untuk_atlet(request):
    return render(request, 'daftar_sponsor_untuk_atlet.html')

def list_sponsor(request):
    sponsor = get_query("""
    SELECT s.nama_brand, sa.tgl_mulai, sa.tgl_selesai FROM SPONSOR s, ATLET_SPONSOR sa, ATLET a WHERE s.id = sa.id_sponsor AND sa.id_atlet = a.id
    """) # NANTI GANTI sa.id_atlet = a.id JADI sa.id_atlet = logged_in_user.id

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