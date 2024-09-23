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
    path("ads.txt/", views.ads, name="ads"),
    path("robots.txt/", views.robots_txt, name="robots"),
    path('oto_masalkategoriekle/', views.oto_masalkategoriekle, name='oto_masalkategoriekle'),
    path('oto_hikayekategoriekle/', views.oto_hikayekategoriekle, name='oto_hikayekategoriekle'),

    path("saglik-add/", views.ai_add, name="saglikadd"),
    path("cocuk-masallari/", views.Masallar, name="MasallarHome"),
    path("Oto_Paylas/", views.Oto_Paylas, name="Oto_Paylas"),
    path("Blog_Paylas/", views.Blog_oto_Paylas, name="Blog_Paylas"),
    path("index-ver/", views.indexing_var_mi, name="indexver"),
    path("blog-index-ver/", views.blog_indexing_var_mi, name="blogindexver"),
    path("facebook-cek/", views.facebook_var_mi, name="facebookcek"),
    path("twitter-cek/", views.twitter_var_mi, name="twittercek"),
    path("pint-cek/", views.pintres_var_mi, name="pintcek"),
    path("masal-hikaye-ekle/", views.ekle, name="masal-hikaye-ekle"),
    path("api-masal-hikaye-ekle/", views.apiyle_ekle, name="api-masal-hikaye-ekle"),

    path("oyunlar/", views.oyunlar, name="oyunlar"),
    path("cocuklara-matematik-oyunu/", views.matematik, name="matematikoyunu"),
    path("cocuklara-hayvan-oyunu/", views.hayvanoyunu, name="hayvanoyunu"),
    path("cocuk-hikayeleri/", views.Hikayeler, name="HikayelerHome"),
    # path("cocuk/", views.BlogHome, name="cocuk"),
    path("cocuk-gelisimi/", views.BlogHome, name="cocuk"),
    path("saglik/", views.BlogHome, name="saglik"),
    path("kadin/", views.BlogHome, name="kadin"),
    path('api/flutter-icerikler/', views.flutter_icerik_api, name='flutter_icerik_api'),
    path('api/flutter-icerik-detay/<slug:slug>/', views.flutter_icerik_detay_api, name='flutter_icerik_detay_api'),

    path("iletisim/", views.iletisim, name="iletisim"),
    path("cerez-politikasi/", views.cerez, name="cerez"),
    path("hakkimizda/", views.hakkimizda, name="hakkimizda"),
    path("gizlilik-politikasi/", views.gizlilik, name="gizlilik-politikasi"),
    path("kullanim-sartlari/", views.kullanim, name="kullanim-sartlari"),

    # path('cocuk-gelisimi/<str:blog_slug>/', views.enderunBlog, name='blog-getir'),
    path('masal-oku/', views.MasalOkuListesi, name='masal-oku'),
    path('hikaye-oku/', views.hikayeOkuListesi, name='hikaye-oku'),
    path('masal-oku/<str:masal_slug>/', views.enderunMasal, name='masal-getir'),
    path('hikaye-oku/<str:hikaye_slug>/', views.enderunHikaye, name='hikaye-getir'),

    path('masal-kategori/<str:alt_kategori_slug>/', views.masalAltKategori, name='masalAltKategori'),
    path('hikaye-kategori/<str:alt_kategori_slug>/', views.hikayeAltKategori, name='hikayeAltKategori'),
    path('<str:blog_slug>/', views.enderunBlog, name='blog-getir'),
]
