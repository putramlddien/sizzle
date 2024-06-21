from django.contrib.auth.models import User
from django.db import models

class KategoriKursus(models.Model):
    id_kategori_kursus = models.AutoField(primary_key=True)
    kategori_kursus = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.kategori_kursus
    
class Kursus(models.Model):
    id_kursus = models.AutoField(primary_key=True)
    id_kegiatan = models.IntegerField(null=True, blank=True, unique=True)
    nama_kursus = models.CharField(max_length=50, unique=True)
    deskripsi_singkat = models.TextField(null=True, blank=True)
    chef = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    harga_kursus = models.IntegerField(default=0)
    gambar_kursus = models.ImageField(upload_to='images/kursus/', null=True, blank=True)
    deskripsi_kursus = models.TextField(null=True, blank=True)
    tingkat_kesulitan = models.CharField(max_length=50, null=True, blank=True)
    tanggal_mulai = models.DateField(null=True, blank=True)
    tanggal_selesai = models.DateField(null=True, blank=True)
    materi_kursus = models.TextField(null=True, blank=True)
    jumlah_peserta = models.IntegerField(default=0)
    syarat_pendaftaran = models.TextField(null=True, blank=True)
    kategori_kursus = models.ForeignKey('KategoriKursus', on_delete=models.CASCADE, related_name='kursuss', default=1)
    

    def __str__(self):
        return self.nama_kursus
    
class UserKursus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.kursus.nama_kursus}"
    


class Pertemuan(models.Model):
    kursus = models.ForeignKey(Kursus, related_name='pertemuans', on_delete=models.CASCADE)
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    tanggal = models.DateField()

    def __str__(self):
        return self.judul

class KontenKursus(models.Model):
    pertemuan = models.ForeignKey(Pertemuan, related_name='konten_kursus', on_delete=models.CASCADE)
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    video = models.FileField(upload_to='videos/kursus/')
    pdf = models.FileField(upload_to='pdfs/kursus/', null=True, blank=True)

    def __str__(self):
        return self.judul

class Tugas(models.Model):
    pertemuan = models.ForeignKey(Pertemuan, related_name='tugas_set', on_delete=models.CASCADE)
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    deadline = models.DateTimeField()

    def __str__(self):
        return self.judul

class Kuis(models.Model):
    pertemuan = models.ForeignKey(Pertemuan, related_name='kuis_set', on_delete=models.CASCADE)
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()

    def __str__(self):
        return self.judul

class Bahan(models.Model):
    pertemuan = models.ForeignKey(Pertemuan, related_name='resep_bahan', on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    jumlah = models.CharField(max_length=50)

    def __str__(self):
        return self.nama
    
class UserKonten(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    konten = models.ForeignKey(KontenKursus, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.konten.judul} - {'Completed' if self.completed else 'Not Completed'}"
    
class KategoriResep(models.Model):
    id_kategori_resep = models.AutoField(primary_key=True)
    kategori_resep = models.CharField(max_length=50, unique=True)
    gambar_kategori_resep = models.ImageField(upload_to='images/resep/', null=True, blank=True)

    def __str__(self):
        return self.kategori_resep


class Resep(models.Model):
    id_resep = models.AutoField(primary_key=True)
    nama_resep = models.CharField(max_length=50, unique=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    durasi = models.IntegerField(default=0)
    porsi = models.IntegerField(default=0)
    gambar_resep = models.ImageField(upload_to='images/resep/', null=True, blank=True)
    definisi = models.TextField(null=True, blank=True)
    bahan = models.TextField(null=True, blank=True)
    informasi_nutrisi = models.TextField(null=True, blank=True)
    cara_membuat = models.TextField(null=True, blank=True)
    kategori_resep = models.ForeignKey('KategoriResep', on_delete=models.CASCADE, related_name='reseps', default=1)
    

    def __str__(self):
        return self.nama_resep


class Artikel(models.Model):
    id_artikel = models.AutoField(primary_key=True)
    judul_artikel = models.CharField(max_length=255, null=True, blank=True)
    penulis = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    isi_artikel = models.TextField(null=True, blank=True)
    tanggal_upload = models.DateTimeField(null=True, blank=True)
    kategori_artikel = models.CharField(max_length=100, null=True, blank=True)
    gambar_artikel = models.ImageField(upload_to='images/artikel/', null=True, blank=True)

    def __str__(self):
        return self.judul_artikel
    

class KategoriTeknik(models.Model):
    id_kategori_teknik = models.AutoField(primary_key=True)
    kategori_teknik = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.kategori_teknik
    
class Teknik(models.Model):
    id_teknik = models.AutoField(primary_key=True)
    judul_teknik = models.CharField(max_length=50, unique=True)
    tipe_artikel = models.CharField(max_length=50, null=True, blank=True)
    penulis = models.CharField(max_length=50, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    isi_artikel = models.TextField(null=True, blank=True)
    tanggal_upload = models.DateTimeField(null=True, blank=True)
    gambar_artikel = models.ImageField(upload_to='images/teknik/', null=True, blank=True)
    kategori_teknik = models.ForeignKey('KategoriTeknik', on_delete=models.CASCADE, related_name='tekniks', default=1)
    
    def __str__(self):
        return self.judul_teknik