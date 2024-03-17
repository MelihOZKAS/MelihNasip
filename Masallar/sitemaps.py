from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.shortcuts import render,HttpResponse,get_object_or_404,reverse
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



class PeriMasallariSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        #alt_kategori = MasalKategorileri.objects.filter(MasalSlug="peri-masallari")
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="peri-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",Model="Masal").order_by('-olusturma_tarihi')


    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])