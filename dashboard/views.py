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
    info_ujian_kualifikasi = get_query("""
    SELECT u.tahun, u.batch, u.tempat, u.tanggal
    FROM UJIAN_KUALIFIKASI u
    """)

    context = {
        'info_ujian_kualifikasi': info_ujian_kualifikasi,
    }

    return render(request, 'tes_kualifikasi.html', context)

def pertanyaan_kualifikasi(request):
    return render(request, 'pertanyaan_kualifikasi.html')

def list_ujian_kualifikasi(request):
    info_ujian_kualifikasi = get_query("""
    SELECT u.tahun, u.batch, u.tempat, u.tanggal
    FROM UJIAN_KUALIFIKASI u
    """)

    context = {
        'info_ujian_kualifikasi': info_ujian_kualifikasi,
    }

    return render(request, 'list_ujian_kualifikasi.html', context)

def create_ujian_kualifikasi(request):
    return render(request, 'create_ujian_kualifikasi.html')

def list_atlet_create(request):
    id_user = request.session['user_id']
    if request.method != 'POST':
        return list_atlet_create_fail(request, False)
    
    nama_atlet = request.POST.get("nama_atlet")
    if not nama_atlet:
        return list_atlet_create_fail(request, True)        
    
    id_atlet = str(get_query(f"SELECT ID FROM MEMBER WHERE Nama='{nama_atlet}';")[0]["id"])

    get_query(f"INSERT INTO ATLET_PELATIH VALUES ('{id_user}', '{id_atlet}');")
    return render(request, 'list_atlet_pelatih.html')

def list_atlet_create_fail(request, fail):
    list_atlet = get_query("SELECT M.Nama FROM MEMBER M, ATLET A WHERE M.ID=A.ID;")
    context = {
        "list_atlet": list_atlet,
        "fail": False
    }
    if fail:
        context["fail"] = True
    return render(request, "list_atlet_create.html", context)

def list_atlet_pelatih(request):
    id_user = request.session['user_id']
    atlet_dilatih = get_query("""SELECT MA.Nama, MA.Email, A.World_rank
                        FROM MEMBER MA, MEMBER MP, ATLET A, ATLET_PELATIH AP, PELATIH P 
                        WHERE MA.ID=A.ID
                        AND MP.ID=P.ID
                        AND AP.ID_Pelatih=P.ID
                        AND AP.ID_Atlet=A.ID
                        AND MP.Nama='{}'
                        AND AND a.id =  '{id_atlet}';
                        """.format(id_atlet = id_user))
    context = {
        "atlet_dilatih": atlet_dilatih
    }
    return render(request, 'list_atlet_pelatih.html', context)
    
def list_atlet_umpire(request):
    id_user = request.session['user_id']

    atlet_kualifikasi = get_query("""
    SELECT DISTINCT m.nama, a.tgl_lahir, a.negara_asal, a.play_right, a.height, ak.world_rank, ak.world_tour_rank, a.jenis_kelamin, ph.total_point
    FROM MEMBER m, ATLET a, ATLET_KUALIFIKASI ak, POINT_HISTORY ph
    WHERE m.id = a.id AND a.id = ak.id_atlet
    AND a.id = ph.id_atlet
    AND total_point IN (
        SELECT total_point FROM POINT_HISTORY
        WHERE id_atlet = ph.id_atlet
        ORDER BY (Tahun, Bulan, Minggu_ke) LIMIT 1
    ) AND a.id =  '{id_atlet}'
    """.format(id_atlet = id_user))
    
    atlet_non_kualifikasi = get_query("""
    SELECT DISTINCT m.nama, a.tgl_lahir, a.negara_asal, a.play_right, a.height, a.world_rank, a.jenis_kelamin,  ph.total_point
    FROM MEMBER m, ATLET a, ATLET_NON_KUALIFIKASI ank, POINT_HISTORY ph
    WHERE m.id = a.id AND a.id = ank.id_atlet AND a.id = ph.id_atlet 
    AND total_point IN (
        SELECT total_point FROM POINT_HISTORY
        WHERE id_atlet = ph.id_atlet
        ORDER BY (Tahun, Bulan, Minggu_ke) LIMIT 1
    ) AND a.id =  '{id_atlet}'                 
    """.format(id_atlet = id_user))
    
    get_query("""
    CREATE VIEW NAMA1 AS
    SELECT ag.id_atlet_ganda, ak.id_atlet, m.nama
    FROM MEMBER m, ATLET_KUALIFIKASI ak, ATLET_GANDA ag, ATLET a
    WHERE m.id = a.id and a.id = ak.id_atlet and ak.id_atlet = ag.id_atlet_kualifikasi and a.id =  '{id_atlet}'
    """.format(id_atlet = id_user))
    
    get_query("""
    CREATE VIEW NAMA2 AS
    SELECT ag.id_atlet_ganda, ak.id_atlet, m.nama
    FROM MEMBER m, ATLET_KUALIFIKASI ak, ATLET_GANDA ag, ATLET a
    WHERE m.id = a.id and a.id = ak.id_atlet and ak.id_atlet = ag.id_atlet_kualifikasi_2 and a.id =  '{id_atlet}'
    """.format(id_atlet = id_user))
    
    atlet_ganda = get_query("""
    SELECT n1.id_atlet_ganda, n1.nama as nama1, n2.nama as nama2, SUM(pha.total_point + phb.total_point) as sum_total_point
    FROM NAMA1 n1, NAMA2 n2, POINT_HISTORY pha, POINT_HISTORY phb
    WHERE n1.id_atlet_ganda = n2.id_atlet_ganda AND pha.id_atlet = n1.id_atlet AND phb.id_atlet = n2.id_atlet
    AND pha.total_point IN (
        SELECT total_point FROM POINT_HISTORY
        WHERE id_atlet = n1.id_atlet
        ORDER BY Tahun, Bulan, Minggu_ke LIMIT 1
    )
    AND phb.total_point IN (
        SELECT total_point FROM POINT_HISTORY
        WHERE id_atlet = n2.id_atlet
        ORDER BY Tahun, Bulan, Minggu_ke LIMIT 1
    )
    AND n1.id_atlet =  '{id_atlet}'
    GROUP BY n1.id_atlet_ganda, n1.nama, n2.nama
    """.format(id_atlet = id_user))
    
    context = {
        'atlet_kualifikasi_list': atlet_kualifikasi,
        'atlet_non_kualifikasi_list' : atlet_non_kualifikasi, 
        'atlet_ganda_list' : atlet_ganda,
    }
    print (context)
    return render(request, 'list_atlet_umpire.html', context)

def daftar_event(request):
    if request.session['role'] == 'atlet':
        if request.session['qualified'] == False:
            messages.error(request, 'Halaman ini hanya bisa diakses atlet terkualifikasi')
            return redirect('/atlet')
    id_user = request.session['user_id']
    list_stadium = get_query("""
    SELECT nama_stadium, negara, kapasitas
    FROM STADIUM st, ATLET a
    WHERE a.id_atlet = '{id_atlet}'
    """.format(id_atlet=id_user))
    context = {
        'list_stadium': list_stadium,
    }
    return render(request, 'daftar_event.html', context)

def daftar_event2(request):
    id_user = request.session['user_id']
    list_event = get_query("""
    SELECT E.nama_event, E.total_hadiah, E.kategori_superseries, S.kapasitas
    FROM EVENT E, STADIUM S, ATLET A
    WHERE S.nama = E.nama_stadium AND A.id_atlet = '{id_atlet}'
    """.format(id_atlet=id_user))
    context = {
        'list_event': list_event,
    }
    return render(request, 'daftar_event2.html', context)

def pilih_kategori(request):
    return render(request, 'pilih_kategori.html')

def read_list_event(request):
    partai_kompetisi = get_query("""SELECT E.Nama_event, E.Tahun, E.Nama_stadium, PK.Jenis_partai,
    E.Kategori_Superseries, E.Tgl_mulai, E.Tgl_selesai, COUNT(PPK.nomor_peserta) AS jumlah_peserta, S.Kapasitas
    FROM EVENT E, PARTAI_KOMPETISI PK, PARTAI_PESERTA_KOMPETISI PPK, STADIUM S
    WHERE E.Nama_event=PK.Nama_event
    AND E.Tahun=PK.Tahun_event
    AND PK.Nama_event=PPK.Nama_event
    AND PK.Tahun_event=PPK.Tahun_event
    AND PK.Jenis_partai=PPK.Jenis_partai
    AND E.Nama_stadium=S.Nama
    GROUP BY E.Nama_event, E.Tahun, E.Nama_stadium, PK.Jenis_partai,
    E.Kategori_Superseries, E.Tgl_mulai, E.Tgl_selesai, S.Kapasitas;
    """)
    context = {
        "partai_kompetisi": partai_kompetisi
    }
    # print (partai_kompetisi)
    return render(request, 'read_list_event.html', context)

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
    
    
def partai_kompetisi_event(request):
    partai_kompetisi = get_query("""SELECT E.Nama_event, E.Tahun, E.Nama_stadium, PK.Jenis_partai,
    E.Kategori_Superseries, E.Tgl_mulai, E.Tgl_selesai, COUNT(PPK.nomor_peserta) AS jumlah_peserta, S.Kapasitas
    FROM EVENT E, PARTAI_KOMPETISI PK, PARTAI_PESERTA_KOMPETISI PPK, STADIUM S
    WHERE E.Nama_event=PK.Nama_event
    AND E.Tahun=PK.Tahun_event
    AND PK.Nama_event=PPK.Nama_event
    AND PK.Tahun_event=PPK.Tahun_event
    AND PK.Jenis_partai=PPK.Jenis_partai
    AND E.Nama_stadium=S.Nama
    GROUP BY E.Nama_event, E.Tahun, E.Nama_stadium, PK.Jenis_partai,
    E.Kategori_Superseries, E.Tgl_mulai, E.Tgl_selesai, S.Kapasitas;
    """)
    request.session['nama_event'] = partai_kompetisi[0]['nama_event']
    context = {
        "partai_kompetisi": partai_kompetisi
    }
    return render(request, 'partai_kompetisi_event.html', context)