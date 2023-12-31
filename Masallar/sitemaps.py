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

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])

    #def youtube(self, obj):
    #    return obj.youtube if obj.youtube else None



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



class CocukSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Blog.objects.filter(aktif=True,status="Yayinda")
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('blog-getir', args=[obj.slug])

    #def youtube(self, obj):
    #    return obj.youtube if obj.youtube else None


#class YouTubeSitemapHikaye(Sitemap):
#    def items(self):
#        return SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").exclude(youtube__isnull=True).exclude(youtube__exact='')
#
#    def location(self, obj):
#        site_url = 'http://www.cocukmasallarioku.com'
#        youtube_url = obj.youtube
#        return site_url + youtube_url
#
#
#class YouTubeSitemapMasal(Sitemap):
#    changefreq = "daily"
#    priority = 0.9
#    protocol = 'https'
#
#    def items(self):
#        return SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal", youtube__isnull=False)
#    def location(self, obj):
#        return reverse(obj.youtube)
#