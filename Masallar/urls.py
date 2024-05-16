
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


from Hepsi.views import *
from .feed import *





def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response

urlpatterns = [
    path("yonetici/", admin.site.urls),

    path("", include("Hepsi.urls")),
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

    path('feeds/dini-hikayeler/', DiniHikayelerFeed(), name='dini_hikayeler_feed'),
    path('feeds/sihirli-dunya-hikayeleri/', SihirliDunyaHikayelerFeed(), name='sihirli_hikayeler_feed'),
    path('feeds/sevimli-hayvan-hikayeleri/', SevimliHayvanHikayelerFeed(), name='hayvan_hikayeler_feed'),
    path('feeds/korkusuz-kahraman-hikayeleri/', KahramanHikayelerFeed(), name='kahraman_hikayeler_feed'),
    path('feeds/mutlu-aile-hikayeleri/', AileHikayelerFeed(), name='aile_hikayeler_feed'),
    path('feeds/hazine-avi-hikayeleri/', HazineHikayelerFeed(), name='hazine_hikayeler_feed'),
    path('feeds/eglenceli-yolculuk-hikayeleri/', YolculukHikayelerFeed(), name='yolculuk_hikayeler_feed'),
    path('feeds/gezi-maceralari-hikayeleri/', GezikHikayelerFeed(), name='gezi_hikayeler_feed'),
    path('feeds/uzay-maceralari-hikayeleri/', UzayHikayelerFeed(), name='gezi_hikayeler_feed'),
    path('feeds/muhtesem-bilim-hikayeleri/', BilimHikayelerFeed(), name='bilim_hikayeler_feed'),
    path('feeds/dostluk-hikayeleri/', DostlukHikayelerFeed(), name='Dostluk_hikayeler_feed'),
    path('feeds/doga-ve-cevre-onemi-hikayeleri/', CevreHikayelerFeed(), name='doga_hikayeler_feed'),
    path('feeds/ingilizce-hikayeler/', ingilizceHikayelerFeed(), name='ingilizce_hikayeler_feed'),
    path('feeds/sevimli-canavar-hikayeleri/', CanavarHikayelerFeed(), name='canavar_hikayeler_feed'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
