# Generated by Django 5.0.6 on 2024-05-28 20:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_delete_kategorikursus'),
    ]

    operations = [
        migrations.CreateModel(
            name='KategoriKursus',
            fields=[
                ('id_kategori_kursus', models.AutoField(primary_key=True, serialize=False)),
                ('kategori_kursus', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='kursus',
            name='kategori_kursus',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='kursuss', to='app.kategorikursus'),
        ),
    ]