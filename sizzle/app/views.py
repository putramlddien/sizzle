from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Kursus, Resep, Teknik, Artikel, KategoriResep, KategoriKursus, UserKursus, Pertemuan, KontenKursus, UserKonten, Tugas, Kuis
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from haystack.query import SearchQuerySet

def search(request):
    query = request.GET.get('q', '')
    kursus_results = SearchQuerySet().models(Kursus).filter(content=query)
    resep_results = SearchQuerySet().models(Resep).filter(content=query)
    context = {
        'kursus_results': kursus_results,
        'resep_results': resep_results,
        'query': query,
    }
    return render(request, 'search_results.html', context)


def index(request):
    kursus_diskon_list = Kursus.objects.filter(harga_kursus__lte=50000)
    resep_populer_list = Resep.objects.filter(rating=5.0)[:6]
    artikel_list = Artikel.objects.order_by('-tanggal_upload')[:3]

    if artikel_list:
        home_artikel = artikel_list[0]
        other_artikel = artikel_list[1:3]
    else:
        home_artikel = None
        other_artikel = []

    context = {
        'resep_populer_list': resep_populer_list,
        'kursus_diskon_list': kursus_diskon_list,
        'home_artikel': home_artikel,
        'other_artikel': other_artikel,
        
    }
    
    return render(request, 'index.html', context)

def kursus(request):
    kategori_id = request.GET.get('kategori')
    if kategori_id:
        kategori = get_object_or_404(KategoriKursus, id_kategori_kursus=kategori_id)
        kursuss = Kursus.objects.filter(kategori_kursus=kategori)
    else:
        kursuss = Kursus.objects.all()
    kategori_kursuss = KategoriKursus.objects.all()
    context = {
        'kursuss': kursuss,
        'kategori_kursuss': kategori_kursuss,
        'selected_kategori_id': kategori_id
    }
    return render(request, 'kursus.html', context)

def detail_kursus(request, id_kursus):
    kursus = get_object_or_404(Kursus, id_kursus=id_kursus)

    context = {
        'kursus': kursus,
    }
    return render(request, 'detail_kursus.html', context)

@login_required
def daftar_kursus(request, id_kursus):
    kursus = get_object_or_404(Kursus, id_kursus=id_kursus)
    user = request.user

    if not UserKursus.objects.filter(user=user, kursus=kursus).exists():
        UserKursus.objects.create(user=user, kursus=kursus)

    return redirect('detail_kursus', id_kursus=id_kursus)

@login_required
def kelas_saya(request):
    user = request.user
    user_kursus = UserKursus.objects.filter(user=user).select_related('kursus')
    context = {
        'user_kursus': user_kursus
    }
    return render(request, 'kelas_saya.html', context)

def calculate_progress(user, kursus):
    total_konten = sum(pertemuan.konten_kursus.count() for pertemuan in kursus.pertemuans.all())
    completed_konten = UserKonten.objects.filter(user=user, konten__pertemuan__kursus=kursus, completed=True).count()
    
    if total_konten == 0:
        return 0
    
    progress = (completed_konten / total_konten) * 100
    return progress

@login_required
def detail_kursus_lms(request, id_kursus):
    kursus = get_object_or_404(Kursus, id_kursus=id_kursus)

    if not UserKursus.objects.filter(user=request.user, kursus=kursus).exists():
        return render(request, 'forbidden.html')

    pertemuans = kursus.pertemuans.all()
    progress = calculate_progress(request.user, kursus)

    context = {
        'kursus': kursus,
        'pertemuans': pertemuans,
        'progress': progress
    }

    return render(request, 'detail_kursus_lms.html', context)

@login_required
def mark_konten_completed(request, id_konten):
    konten = get_object_or_404(KontenKursus, id=id_konten)
    user_konten, created = UserKonten.objects.get_or_create(user=request.user, konten=konten)
    user_konten.completed = True
    user_konten.save()
    
    return redirect('detail_kursus_lms', id_kursus=konten.pertemuan.kursus.id)

@login_required
def submit_tugas(request, id_tugas):
    tugas = get_object_or_404(Tugas, id=id_tugas)
    if request.method == 'POST':
        # Handle file upload for task submission
        # file = request.FILES['file']
        # Save file or handle submission
        return redirect('detail_kursus_lms', id_kursus=tugas.pertemuan.kursus.id)

    return render(request, 'submit_tugas.html', {'tugas': tugas})

@login_required
def ambil_kuis(request, id_kuis):
    kuis = get_object_or_404(Kuis, id=id_kuis)
    if request.method == 'POST':
        # Handle quiz submission
        return redirect('detail_kursus_lms', id_kursus=kuis.pertemuan.kursus.id)

    return render(request, 'ambil_kuis.html', {'kuis': kuis})


def resep(request):
    kategori_id = request.GET.get('kategori')
    if kategori_id:
        kategori = get_object_or_404(KategoriResep, id_kategori_resep=kategori_id)
        reseps = Resep.objects.filter(kategori_resep=kategori)
    else:
        reseps = Resep.objects.all()
    kategori_reseps = KategoriResep.objects.all()
    context = {
        'reseps': reseps,
        'kategori_reseps': kategori_reseps,
        'selected_kategori_id': kategori_id
    }
    return render(request, 'resep.html', context)


def detail_resep(request, id_resep):
    resep = get_object_or_404(Resep, id_resep=id_resep)
    bahan_list = resep.bahan.split('\n')
    langkah_cara_membuat = resep.cara_membuat.split('\n')

    return render(request, 'detail_resep.html', {
        'resep': resep,
        'bahan_list': bahan_list,
        'informasi_nutrisi': resep.informasi_nutrisi,
        'langkah_cara_membuat': langkah_cara_membuat
    })

def kategori_resep(request):
    return render(request, )

def coming_soon(request):
    return render(request, 'coming_soon.html')

def nilai_kuis(request):
    return render(request, 'nilai_kuis.html')

def nilai_tugas(request):
    return render(request, 'nilai_tugas.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Email atau password salah'})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        
        if password != repassword:
            return render(request, 'register.html', {'error_message': 'Password tidak cocok'})

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return redirect('login')
    return render(request, 'register.html')

def logout(request):
    auth_logout(request)
    return redirect('index')

def base(request):
    return render(request, 'base.html')

def base_user(request):
    return render(request, 'base_user.html')

def teknik(request):
    teknik_utama = Teknik.objects.filter(tipe_artikel='teknik_utama').order_by('-tanggal_upload')

    context = {
        'teknik_utama': teknik_utama,
    }

    return render(request, 'teknik.html' , context)

def teknik_memasak(request, kategori):
    teknik_utama = Teknik.objects.filter(
        kategori_teknik__kategori_teknik=kategori,
        tipe_artikel='teknik_utama'
    ).order_by('-tanggal_upload')

    sub_teknik = Teknik.objects.filter(
        kategori_teknik__kategori_teknik=kategori,
        tipe_artikel='sub_teknik'
    ).order_by('-tanggal_upload')

    context = {
        'teknik_utama': teknik_utama,
        'sub_teknik': sub_teknik,
        'kategori': kategori,
    }

    return render(request, 'teknik_memasak.html', context)

def artikel(request):
    art = Artikel.objects.filter(kategori_artikel='food-art')
    edukasi = Artikel.objects.filter(kategori_artikel='edukasi')
    artikel = Artikel.objects.filter(kategori_artikel='artikel')
    return render(request, 'artikel.html', {'food_art': art, 'edukasi': edukasi, 'artikel': artikel})
