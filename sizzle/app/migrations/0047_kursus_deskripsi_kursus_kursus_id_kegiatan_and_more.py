# Generated by Django 5.0.6 on 2024-05-30 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_teknik_tipe_artikel'),
    ]

    operations = [
        migrations.AddField(
            model_name='kursus',
            name='deskripsi_kursus',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='kursus',
            name='id_kegiatan',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='kursus',
            name='jumlah_peserta',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='kursus',
            name='materi_kursus',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='kursus',
            name='syarat_pendaftaran',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='kursus',
            name='tanggal_mulai',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='kursus',
            name='tanggal_selesai',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='kursus',
            name='tingkat_kesulitan',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]