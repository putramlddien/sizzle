# Generated by Django 5.0.6 on 2024-05-20 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_artikel_id_artikel_remove_kursus_harga_kursus_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artikel',
            name='id',
        ),
        migrations.RemoveField(
            model_name='kursus',
            name='id',
        ),
        migrations.RemoveField(
            model_name='resep',
            name='id',
        ),
        migrations.AddField(
            model_name='artikel',
            name='id_artikel',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kursus',
            name='id_kursus',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resep',
            name='id_resep',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]