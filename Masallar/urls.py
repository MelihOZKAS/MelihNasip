
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import index, sitemap
from .sitemaps import *
from Hepsi.views import *
from .feed import *



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

def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response

urlpatterns = [
    path("yonetici/", admin.site.urls),
    path("", include("Hepsi.urls")),
    path("robots.txt/",robots_txt, name="robots"),
    path("Ads.txt/",ads, name="ads"),
    path("ads.txt/",ads, name="ads"),

    path('sitemap.xml/', index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('feeds/dini-masallar/', DiniMasallarFeed(), name='dini_masal_feed'),
    path('feeds/peri-masallari/', PeriMasallariFeed(), name='peri_masal_feed'),
    path('feeds/uyku-masallari/', UykuMasallariFeed(), name='uyku_masallari_feed'),
    path('feeds/hayvan-masallari/', HayvanMasallariFeed(), name='hayvan_masallari_feed'),
    path('feeds/prenses-masallari/', PrensesMasallariFeed(), name='prenses_masallari_feed'),
    path('feeds/prens-masallari/', PrensMasallariFeed(), name='prens_masallari_feed'),
    path('feeds/aile-masallari/', AileMasallariFeed(), name='aie_masallari_feed'),
    path('feeds/macera-masallari/', MaceraMasallariFeed(), name='macera_masallari_feed'),
    path('feeds/komik-masallar/', KomikMasallariFeed(), name='komik_masallari_feed'),
    path('feeds/egitici-masallar/', EgiticiMasallariFeed(), name='egitici_masallari_feed'),
    path('feeds/arkadas-masallari/', ArkadasMasallariFeed(), name='arkadas_masallari_feed'),
    path('feeds/kardeslik-masallari/', KardesMasallariFeed(), name='kardeslik_masallari_feed'),
    path('feeds/iyilik-masallari/', iyilikMasallariFeed(), name='iyilik_masallari_feed'),
    path('feeds/keloglan-masallari/', KeloglanMasallariFeed(), name='keloglan_masallari_feed'),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
