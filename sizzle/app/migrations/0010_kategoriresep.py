# Generated by Django 5.0.6 on 2024-05-27 10:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_resep_bahan_resep_cara_membuat_resep_definisi_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='KategoriResep',
            fields=[
                ('id_kategori_resep', models.AutoField(primary_key=True, serialize=False)),
                ('kategori_resep', models.CharField(max_length=50, unique=True)),
                ('nama_resep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kategoris', to='app.resep')),
            ],
        ),
    ]
