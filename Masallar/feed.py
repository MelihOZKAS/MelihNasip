from django.contrib.syndication.views import Feed
from django.urls import reverse
from Hepsi.models import *
from django.shortcuts import render,HttpResponse,get_object_or_404,reverse




class DiniMasallarFeed(Feed):
    title = "Dini Masallar"
    link = "/feeds/dini-masallar/"
    description = "En son eklenen dini masallar."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="dini-masallar")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"



class PeriMasallariFeed(Feed):
    title = "Peri Masalları"
    link = "/feeds/peri-masallari/"
    description = "En son eklenen peri masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="peri-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"


class UykuMasallariFeed(Feed):
    title = "Uyku Masalları"
    link = "/feeds/uyku-masallari/"
    description = "En son eklenen uyku masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="uyku-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"

class HayvanMasallariFeed(Feed):
    title = "Sevimli Hayvan Masalları"
    link = "/feeds/hayvan-masallari/"
    description = "En son eklenen sevimli hayvan masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="hayvan-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"

class PrensesMasallariFeed(Feed):
    title = "Prenses Masalları"
    link = "/feeds/prenses-masallari/"
    description = "En son eklenen prenses masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="prenses-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"

class PrensMasallariFeed(Feed):
    title = "Prens Masalları"
    link = "/feeds/prens-masallari/"
    description = "En son eklenen prens masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="prens-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"

class AileMasallariFeed(Feed):
    title = "Aile Masalları"
    link = "/feeds/aile-masallari/"
    description = "En son eklenen aile masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="aile-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"


class MaceraMasallariFeed(Feed):
    title = "Macera Masalları"
    link = "/feeds/macera-masallari/"
    description = "En son eklenen macera masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="macera-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"



class KomikMasallariFeed(Feed):
    title = "Komik Masallar"
    link = "/feeds/komik-masallar/"
    description = "En son eklenen komik masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="komik-masallar")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"


class EgiticiMasallariFeed(Feed):
    title = "Eğitici Masallar"
    link = "/feeds/egitici-masallar/"
    description = "En son eklenen eğitici masallar."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="egitici-masallar")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"



class ArkadasMasallariFeed(Feed):
    title = "Arkadaş Masallar"
    link = "/feeds/arkadas-masallari/"
    description = "En son eklenen arkadaş masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="arkadas-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"

class KardesMasallariFeed(Feed):
    title = "Kardeşlik Masalları"
    link = "/feeds/kardeslik-masallari/"
    description = "En son eklenen kardeş masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="kardeslik-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"

class iyilikMasallariFeed(Feed):
    title = "iyilik Masalları"
    link = "/feeds/iyilik-masallari/"
    description = "En son eklenen iyilik doğruluk masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="iyilik-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"


class KeloglanMasallariFeed(Feed):
    title = "Keloğşan Masalları"
    link = "/feeds/keloglan-masallari/"
    description = "En son eklenen keloğlan masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="keloglan-masallari")
        return SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Masal").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('masal-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"


class DiniHikayelerFeed(Feed):
    title = "Dini Hikayeler"
    link = "/feeds/dini-hikayeler/"
    description = "En son eklenen dini hikayeler."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="dini-hikayeler")
        return SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                        Model="Hikaye").order_by('-olusturma_tarihi')[:20]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.meta_description
    def item_link(self, item):
        return reverse('hikaye-getir', args=[item.slug])
    def item_pubdate(self, item):
        return item.olusturma_tarihi
    def item_author_name(self, item):
        return "Melih ÖZKAŞ"
















