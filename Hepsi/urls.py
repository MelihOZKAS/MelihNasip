"""
URL configuration for Masallar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('oto_masalkategoriekle/', views.oto_masalkategoriekle, name='oto_masalkategoriekle'),
    path('oto_hikayekategoriekle/', views.oto_hikayekategoriekle, name='oto_hikayekategoriekle'),

    path("cocuk-masallari/", views.Masallar, name="MasallarHome"),
    path("Oto_Paylas/", views.Oto_Paylas, name="Oto_Paylas"),
    path("masal-hikaye-ekle/", views.ekle, name="masal-hikaye-ekle"),


    path("cocuk-hikayeleri/", views.Hikayeler, name="HikayelerHome"),
    #path("cocuk/", views.BlogHome, name="cocuk"),
    path("cocuk-gelisimi/", views.BlogHome, name="cocuk"),

    path("iletisim/", views.iletisim, name="iletisim"),
    path("hakkimizda/", views.hakkimizda, name="hakkimizda"),
    path("gizlilik-politikasi/", views.gizlilik, name="gizlilik-politikasi"),
    path("kullanim-sartlari/", views.kullanim, name="kullanim-sartlari"),


    path('cocuk-gelisimi/<str:blog_slug>/', views.enderunBlog, name='blog-getir'),
    path('masal-oku/<str:masal_slug>/', views.enderunMasal, name='masal-getir'),
    path('hikaye-oku/<str:hikaye_slug>/', views.enderunHikaye, name='hikaye-getir'),



    path('masal-kategori/<str:alt_kategori_slug>/', views.masalAltKategori, name='masalAltKategori'),
    path('hikaye-kategori/<str:alt_kategori_slug>/', views.hikayeAltKategori, name='hikayeAltKategori'),

]
