"""
URL configuration for sizzle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('kursus.html', views.kursus, name='kursus'),
    path('resep.html', views.resep, name='resep'),
    path('resep/<int:id_resep>/', views.detail_resep, name='detail_resep'),
    
    path('login.html', views.login, name='login'),
    path('register.html', views.register, name='register'),
    path('base.html', views.base, name='base'),
    path('base_user.html', views.base_user, name='base_user'),
    path('artikel.html', views.artikel, name='artikel'),
    path('teknik_memasak.html', views.teknik_memasak, name='teknik_memasak'),
    path('teknik.html', views.teknik, name='teknik'),

    path('coming_soon.html', views.coming_soon, name='coming_soon'),
    path('kelas_saya.html', views.kelas_saya, name='kelas_saya'),
    path('', include('app.urls')),
    path('admin/', admin.site.urls)
]
