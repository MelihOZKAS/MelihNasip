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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import index, sitemap
from .sitemaps import *
from Hepsi.views import *



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



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
