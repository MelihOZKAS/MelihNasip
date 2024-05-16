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
from django.contrib.sitemaps.views import index, sitemap
from Masallar.sitemaps import *


sitemaps = {
    'masal-kategorileri': MasalKategorileriSitemap,
    'masallar': MasallarSitemap,
    'hikaye-kategorileri': HikayeAltKategoriSitemap,
    'hikayeler': HikayelerSitemap,
    'cocuk-gelisimi': CocukSitemap,
    'dini-masallari': DiniMasallariSitemap,
    'peri-masallari': PeriMasallariSitemap,
    'uyku-masallari': UykuMasallariSitemap,
    'hayvan-masallari': HayvanMasallariSitemap,
    'prenses-masallari': PrensesMasallariSitemap,
    'prens-masallari': PrensMasallariSitemap,
    'aile-masallari': AileMasallariSitemap,
    'macera-masallari': MaceraMasallariSitemap,
    'komik-masallari': KomikMasallariSitemap,
    'egitici-masallari': EgiticiMasallariSitemap,
    'arkadas-masallari': ArkadasMasallariSitemap,
    'kardes-masallari': KardesMasallariSitemap,
    'iyilik-masallari': iyilikMasallariSitemap,
    'keloglan-masallari': KelOglanMasallariSitemap,

    'dini-hikayeler': DiniHikayelerSitemap,
    'sihirli-dunya-hikayeleri': SihirliDunyaHikayelerSitemap,
    'sevimli-hayvan-hikayeleri': SevimliHayvanHikayelerSitemap,
    'kahraman-hikayeleri': KahramanHikayelerSitemap,
    'aile-hikayeleri': AileHikayelerSitemap,
    'hazine-avi-hikayeleri': HazineHikayelerSitemap,
    'eglenceli-yolculuk-hikayeleri': YolculukHikayelerSitemap,
    'gezi-maceralari-hikayeleri': GeziHikayelerSitemap,
    'uzay-maceralari-hikayeleri': UzayHikayelerSitemap,
    'muhtesem-bilim-hikayeleri': BilimHikayelerSitemap,
    'dostluk-hikayeleri': DostlukHikayelerSitemap,
    'doga-ve-cevre-onemi-hikayeleri': DogaHikayelerSitemap,
    'ingilizce-hikayeler': EnglishHikayelerSitemap,
    'sevimli-canavar-hikayeleri': SevimliCanavarHikayelerSitemap,
}

urlpatterns = [
    path("", views.home, name="home"),
    path("ads.txt/", views.ads, name="ads"),
    path("robots.txt/", views.robots_txt, name="robots"),
    path('sitemap.xml/', index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),


    path('oto_masalkategoriekle/', views.oto_masalkategoriekle, name='oto_masalkategoriekle'),
    path('oto_hikayekategoriekle/', views.oto_hikayekategoriekle, name='oto_hikayekategoriekle'),

    path("saglik-add/", views.ai_add, name="saglikadd"),
    path("cocuk-masallari/", views.Masallar, name="MasallarHome"),
    path("Oto_Paylas/", views.Oto_Paylas, name="Oto_Paylas"),
    path("Blog_Paylas/", views.Blog_oto_Paylas, name="Blog_Paylas"),
    path("index-ver/", views.indexing_var_mi, name="indexver"),
    path("blog-index-ver/", views.blog_indexing_var_mi, name="blogindexver"),
    path("facebook-cek/", views.facebook_var_mi, name="facebookcek"),
    path("masal-hikaye-ekle/", views.ekle, name="masal-hikaye-ekle"),
    path("api-masal-hikaye-ekle/", views.apiyle_ekle, name="api-masal-hikaye-ekle"),

    path("cocuk-hikayeleri/", views.Hikayeler, name="HikayelerHome"),
    # path("cocuk/", views.BlogHome, name="cocuk"),
    path("cocuk-gelisimi/", views.BlogHome, name="cocuk"),
    path("saglik/", views.BlogHome, name="saglik"),
    path("kadin/", views.BlogHome, name="kadin"),

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
