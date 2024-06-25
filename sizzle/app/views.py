from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .models import Kursus, Resep, UserResep, Teknik, Artikel, KategoriResep, KategoriKursus, UserKursus, Pertemuan, KontenKursus, UserKonten, Tugas, Kuis, Submission, Kuis, Pertanyaan, Pilihan, HasilKuis
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .forms import SubmissionForm, KuisForm, UserForm, UserProfileForm
from django.utils import timezone


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
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        else:
            print("User Form Errors:", user_form.errors)
            print("Profile Form Errors:", profile_form.errors)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile.html', context)

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
def submit_tugas(request, tugas_id):
    tugas = get_object_or_404(Tugas, id=tugas_id)
    pertemuan = tugas.pertemuan 
    submission = Submission.objects.filter(user=request.user, tugas=tugas).first()

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.tugas = tugas
            submission.pertemuan = pertemuan
            submission.save()
            return redirect('submit_tugas', tugas_id=tugas.id)
    else:
        form = SubmissionForm(instance=submission)
    
    return render(request, 'submit_tugas.html', {'form': form, 'tugas': tugas, 'submission': submission, 'pertemuan': pertemuan})

@login_required
def delete_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, user=request.user)
    tugas_id = submission.tugas.id
    submission.delete()
    return redirect('submit_tugas', tugas_id=tugas_id)

@login_required
def kuis_detail(request, kuis_id):
    kuis = get_object_or_404(Kuis, id=kuis_id)
    user = request.user

    if HasilKuis.objects.filter(user=user, kuis=kuis).exists():
        return redirect('kuis_hasil', kuis_id=kuis.id)

    pertanyaan_set = kuis.pertanyaan_set.all()

    if request.method == 'POST':
        form = KuisForm(request.POST, pertanyaan_set=pertanyaan_set)
        if form.is_valid():
            skor = 0
            for i, pertanyaan in enumerate(pertanyaan_set):
                pilihan_id = form.cleaned_data[f'pertanyaan_{i}']
                pilihan = get_object_or_404(Pilihan, id=pilihan_id)
                if pilihan.benar:
                    skor += 1
            skor_total = (skor / len(pertanyaan_set)) * 100
            HasilKuis.objects.create(user=user, kuis=kuis, skor=skor_total)
            return redirect('kuis_hasil', kuis_id=kuis.id)
    else:
        form = KuisForm(pertanyaan_set=pertanyaan_set)

    context = {
        'kuis': kuis,
        'form': form,
    }
    return render(request, 'kuis_detail.html', context)

@login_required
def kuis_hasil(request, kuis_id):
    kuis = get_object_or_404(Kuis, id=kuis_id)
    hasil = get_object_or_404(HasilKuis, user=request.user, kuis=kuis)
    kursus_id = kuis.pertemuan.kursus.id_kursus

    context = {
        'kuis': kuis,
        'hasil': hasil,
        'kursus_id': kursus_id,
    }
    return render(request, 'kuis_hasil.html', context)


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

@login_required
def simpan_resep(request, id_resep):
    resep = get_object_or_404(Resep, id_resep=id_resep)
    user = request.user

    if not UserResep.objects.filter(user=user, resep=resep).exists():
        UserResep.objects.create(user=user, resep=resep)

    return redirect('detail_resep', id_resep=id_resep)


def resepbookmark(request):
    user = request.user
    user_resep = UserResep.objects.filter(user=user).select_related('resep')
    context = {
        'user_resep': user_resep
    }
    return render(request, 'base.html', context)

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

def detail_artikel(request, id):
    artikel = get_object_or_404(Artikel, id_artikel=id)
    recent_artikels = Artikel.objects.order_by('-tanggal_upload')[:6]
    return render(request, 'detail_artikel.html', {
        'artikel': artikel,
        'recent_artikels': recent_artikels
    })

