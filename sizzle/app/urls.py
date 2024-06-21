from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from .views import search

urlpatterns = [
    path('', views.index, name='index'),
    path('kursus/<int:id_kursus>/', views.detail_kursus, name='detail_kursus'),
    path('detail_kursus_lms/<int:id_kursus>/', views.detail_kursus_lms, name='detail_kursus_lms'),
    path('mark_konten_completed/<int:id_konten>/', views.mark_konten_completed, name='mark_konten_completed'),
    path('submit_tugas/<int:id_tugas>/', views.submit_tugas, name='submit_tugas'),
    path('ambil_kuis/<int:id_kuis>/', views.ambil_kuis, name='ambil_kuis'),
    path('kursus/<int:id_kursus>/daftar/', views.daftar_kursus, name='daftar_kursus'),
    path('kelas-saya/', views.kelas_saya, name='kelas_saya'),
    path('resep/', views.resep, name='resep_list'),
    path('resep/<int:id_resep>/', views.detail_resep, name='detail_resep'),
    path('kategori-resep/', views.kategori_resep, name='kategori_resep'),
    path('coming-soon/', views.coming_soon, name='coming_soon'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('base/', views.base, name='base'),
    path('base_user/', views.base_user, name='base_user'),
    path('teknik-memasak/<str:kategori>/', views.teknik_memasak, name='teknik_memasak'),
    path('artikel/', views.artikel, name='artikel'),
    path('kelas_saya/', views.kelas_saya, name='kelas_saya'),
    path('nilai_kuis/', views.nilai_kuis, name='nilai_kuis'),
    path('nilai_tugas/', views.nilai_tugas, name='nilai_tugas'),
    path('search/', search, name='search'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
