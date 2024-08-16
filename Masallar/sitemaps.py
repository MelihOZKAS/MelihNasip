from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.shortcuts import render,HttpResponse,get_object_or_404,reverse
from Hepsi.models import *

class MasalKategorileriSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.3
    protocol = 'https'

    def items(self):
        return MasalKategorileri.objects.all()

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masalAltKategori', args=[obj.MasalSlug])


class MasallarSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('-guncelleme_tarihi')

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])



class HikayeAltKategoriSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.3
    protocol = 'https'

    def items(self):
        return HikayeKategorileri.objects.all()


    def location(self, obj):
        return reverse('hikayeAltKategori', args=[obj.HikayeSlug])


class HikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by('-guncelleme_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])



class CocukSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Blog.objects.filter(aktif=True, status="Yayinda").order_by('-guncelleme_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('blog-getir', args=[obj.slug])






class DiniMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="dini-masallar")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])
class PeriMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="peri-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])

class UykuMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="uyku-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])

class HayvanMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="hayvan-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])


class PrensesMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="prenses-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])
class PrensMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="prens-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])

class AileMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="aile-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])


class MaceraMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="macera-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])

class KomikMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="komik-masallar")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])


class EgiticiMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="egitici-masallar")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])

class ArkadasMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="arkadas-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])

class KardesMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="kardeslik-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])

class iyilikMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="iyilik-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])

class KelOglanMasallariSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="keloglan-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Masal").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('masal-getir', args=[obj.slug])


class DiniHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="dini-hikayeler")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])


class SihirliDunyaHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="sihirli-dunya-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])

class SevimliHayvanHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="sevimli-hayvan-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])

class KahramanHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="korkusuz-kahraman-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])


class AileHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="mutlu-aile-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])

class HazineHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="hazine-avi-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])

class YolculukHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="eglenceli-yolculuk-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])


class GeziHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="gezi-maceralari-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])

class UzayHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="uzay-maceralari-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])

class BilimHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="muhtesem-bilim-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])

class DostlukHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="dostluk-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])

class DogaHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="doga-ve-cevre-onemi-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])
class EnglishHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="ingilizce-hikayeler")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])

class SevimliCanavarHikayelerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="sevimli-canavar-hikayeleri")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('hikaye-getir', args=[obj.slug])


