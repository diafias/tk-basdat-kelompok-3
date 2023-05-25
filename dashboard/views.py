from django.shortcuts import redirect, render
from project_django.utils import get_query
from django.contrib import messages


# Create your views here.

def dashboard_atlet_page(request):
    info_atlet = get_query("""
    SELECT m.nama, m.email, a.negara_asal, a.tgl_lahir, a.play_right, a.height, a.world_rank, a.jenis_kelamin
    FROM MEMBER m
    JOIN ATLET a ON m.id = a.id
    WHERE m.id = '{id_atlet}'
    """.format(id_atlet = request.session['user_id']))

    info_pelatih = get_query("""
    SELECT m.nama
    FROM MEMBER m
    WHERE m.id IN (
        SELECT ap.id_pelatih
        FROM ATLET_PELATIH ap
        WHERE ap.id_atlet = '{id_atlet}'
    )
    """.format(id_atlet = request.session['user_id']))

    status = get_query("""
    SELECT * from ATLET_KUALIFIKASI WHERE id_atlet = '{id_atlet}'
    """.format(id_atlet = request.session['user_id'])) != []

    request.session['qualified'] = status

    total_point = get_query("""
    SELECT SUM(total_point) AS sum_total_point
    FROM public.point_history
    WHERE id_atlet = '{id_atlet}'
    """.format(id_atlet = request.session['user_id']))

    context = {
        'info_atlet': info_atlet,
        'info_pelatih': info_pelatih,
        'status': status,
        'total_point': total_point[0].sum_total_point,
    }

    return render(request, 'dashboard_atlet_page.html', context)

def dashboard_pelatih_page(request):
    info_pelatih = get_query("""
    SELECT m.nama, m.email, p.tanggal_mulai
    FROM MEMBER m
    JOIN PELATIH p ON m.id = p.id
    WHERE m.id = '{id_pelatih}'
    """.format(id_pelatih = request.session['user_id']))

    info_spesialisasi = get_query("""
    SELECT s.spesialisasi
    FROM PELATIH p
    JOIN PELATIH_SPESIALISASI ps ON p.id = ps.id_pelatih
    JOIN SPESIALISASI s ON ps.id_spesialisasi = s.id
    WHERE p.id = '{id_pelatih}'
    """.format(id_pelatih = request.session['user_id']))

    context = {
        'info_pelatih': info_pelatih,
        'info_spesialisasi': info_spesialisasi,
    }
    return render(request, 'dashboard_pelatih_page.html', context)

def dashboard_umpire_page(request):
    info_umpire = get_query("""
    SELECT m.nama, m.email, u.negara
    FROM MEMBER m
    JOIN UMPIRE u ON m.id = u.id
    WHERE m.id = '{id_umpire}'
    """.format(id_umpire = request.session['user_id']))

    context = {
        'info_umpire': info_umpire,
    }

    return render(request, 'dashboard_umpire_page.html', context)

def tes_kualifikasi(request):
    return render(request, 'tes_kualifikasi.html')

def pertanyaan_kualifikasi(request):
    return render(request, 'pertanyaan_kualifikasi.html')

def daftar_atlet(request):
    return render(request, 'daftar_atlet.html')

def list_atlet(request):
    is_pelatih = request.session['role'] == 'pelatih'
    is_umpire = request.session['role'] == 'umpire'
    context = {
        'is_pelatih': is_pelatih,
        'is_umpire': is_umpire,
    }
    return render(request, 'list_atlet.html', context)

def daftar_event(request):
    # if request.session['role'] == 'atlet':
    #     if request.session['qualified'] == False:
    #         messages.error(request, 'Halaman ini hanya bisa diakses atlet terkualifikasi')
    #         return redirect('/atlet')
    list_stadium = get_query("""
    SELECT nama, negara, kapasitas FROM STADIUM
    """)
    context = {
        'list_stadium': list_stadium,
    }
    return render(request, 'daftar_event.html', context)

def daftar_event2(request):
    list_event = get_query("""
    SELECT E.nama_event, E.total_hadiah, E.kategori_superseries, S.kapasitas
    FROM EVENT E, STADIUM S
    WHERE S.nama = E.nama_stadium AND S.negara = E.negara
    """)
    context = {
        'list_event': list_event,
    }
    return render(request, 'daftar_event2.html', context)

def pilih_kategori(request):
    return render(request, 'pilih_kategori.html')

def read_list_event(request):
    return render(request, 'read_list_event.html')

def hasil_pertandingan_page(request):
    return render(request, 'hasil_pertandingan_page.html')

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

def enrolled_event(request):
    if request.session['role'] == 'atlet':
        if request.session['qualified'] == False:
            messages.error(request, 'Halaman ini hanya bisa diakses atlet terkualifikasi')
            return redirect('/atlet')
        
    id_user = request.session['user_id']

    if request.method == "POST":
        tahun = request.POST.get('tahun')
        nama_event = request.POST.get('event_name')
        
        get_query("""
        DELETE FROM peserta_mendaftar_event
        WHERE tahun = '{tahun}' AND nama_event = '{nama_event}'
        AND nomor_peserta IN (
            SELECT nomor_peserta
            FROM peserta_kompetisi
            WHERE id_atlet_kualifikasi = '{id_atlet}'
            OR id_atlet_ganda IN (
                SELECT id_atlet_ganda
                FROM atlet_ganda
                WHERE id_atlet_kualifikasi = '{id_atlet}'
                OR id_atlet_kualifikasi_2 = '{id_atlet}'
            )
        )
        """.format(tahun = tahun, nama_event = nama_event, id_atlet = id_user))
        


    enrolled_event = get_query("""
    SELECT DISTINCT e.nama_event, e.tahun, e.nama_stadium, e.kategori_superseries, e.total_hadiah, e.tgl_mulai, e.tgl_selesai
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
    if request.session['role'] == 'atlet':
        if request.session['qualified'] == False:
            messages.error(request, 'Halaman ini hanya bisa diakses atlet terkualifikasi')
            return redirect('/atlet')
            
    id_user = request.session['user_id']
    enrolled_partai = get_query("""
    SELECT DISTINCT ppk.nama_event, ppk.tahun_event, ppk.jenis_partai, e.nama_stadium, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai
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
    if request.session['role'] == 'atlet':
        if request.session['qualified'] == False:
            messages.error(request, 'Halaman ini hanya bisa diakses atlet terkualifikasi')
            return redirect('/atlet')        
    id_user = request.session['user_id']

    if request.method == "POST":
        nama_brand = request.POST.get('brand_name')
        tgl_mulai = request.POST.get('start_date')
        tgl_selesai = request.POST.get('end_date')

        id_sponsor = get_query("""
        SELECT id FROM SPONSOR WHERE nama_brand = '{brand}'
        """.format(brand = nama_brand))

        get_query("""
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
    if request.session['role'] == 'atlet':
        if request.session['qualified'] == False:
            messages.error(request, 'Halaman ini hanya bisa diakses atlet terkualifikasi')
            return redirect('/atlet')
        
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
    