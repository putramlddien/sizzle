from django.contrib import admin
from .models import Kursus, Resep, Teknik, Artikel, KategoriResep, KategoriKursus, KategoriTeknik, UserKursus, Pertemuan, KontenKursus, Tugas, Kuis, Bahan, UserKonten, Submission, Kuis, Pertanyaan, Pilihan, HasilKuis

# Register your models here.sizzle123
admin.site.register(Kursus)
admin.site.register(UserKursus)
admin.site.register(Pertemuan)
admin.site.register(KontenKursus)
admin.site.register(Tugas)
admin.site.register(Submission)
admin.site.register(Kuis)
admin.site.register(Pertanyaan)
admin.site.register(Pilihan)
admin.site.register(HasilKuis)
admin.site.register(Bahan)
admin.site.register(UserKonten)
admin.site.register(KategoriKursus)
admin.site.register(Resep)
admin.site.register(Artikel)
admin.site.register(KategoriResep)
admin.site.register(Teknik)
admin.site.register(KategoriTeknik)
