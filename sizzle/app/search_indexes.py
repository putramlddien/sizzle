from haystack import indexes
from .models import Kursus, Resep

class KursusIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nama_kursus = indexes.CharField(model_attr='nama_kursus')
    deskripsi_singkat = indexes.CharField(model_attr='deskripsi_singkat')
    chef = indexes.CharField(model_attr='chef')
    harga_kursus = indexes.IntegerField(model_attr='harga_kursus')

    def get_model(self):
        return Kursus

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class ResepIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nama_resep = indexes.CharField(model_attr='nama_resep')
    definisi = indexes.CharField(model_attr='definisi')
    bahan = indexes.CharField(model_attr='bahan')
    cara_membuat = indexes.CharField(model_attr='cara_membuat')

    def get_model(self):
        return Resep

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
