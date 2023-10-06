from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from Hepsi.models import *

class MasalKategorileriSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.3
    protocol = 'https'

    def items(self):
        return MasalKategorileri.objects.all()

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masalAltKategori', args=[obj.MasalSlug])


class MasallarSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return SiirMasal.objects.filter(aktif=True,status="Yayinda",Model="Masal")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi


    def video(self, obj):
        return {
            'url': obj.youtube,
            # Diğer video meta verilerini buraya ekleyin
        }


    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])





class HikayeAltKategoriSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.3
    protocol = 'https'

    def items(self):
        return HikayeKategorileri.objects.all()


    def location(self, obj):
        return reverse('hikayeAltKategori', args=[obj.HikayeSlug])


class HikayelerSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return SiirMasal.objects.filter(aktif=True,status="Yayinda",Model="Hikaye")
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])

