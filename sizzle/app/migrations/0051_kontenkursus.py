# Generated by Django 5.0.6 on 2024-06-11 18:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_alter_userkursus_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='KontenKursus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(blank=True, max_length=200, null=True)),
                ('deskripsi', models.TextField(blank=True, null=True)),
                ('video_url', models.URLField(blank=True, null=True)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='documents/pdf/')),
                ('tugas', models.TextField(blank=True, null=True)),
                ('kursus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='konten_kursus', to='app.kursus')),
            ],
        ),
    ]