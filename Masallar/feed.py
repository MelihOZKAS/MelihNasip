from django.contrib.syndication.views import Feed
from django.urls import reverse
from Hepsi.models import *
from django.shortcuts import render,HttpResponse,get_object_or_404,reverse




class DiniMasallarFeed(Feed):
    title = "Dini Masallar"
    link = "/feeds/dini_masallar/"
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
    link = "/feeds/peri_masallari/"
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
    link = "/feeds/uyku_masallari/"
    description = "En son eklenen peri masalları."

    def items(self):
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug="uyku_masallari")
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
    link = "/feeds/hayvan_masallari/"
    description = "En son eklenen peri masalları."

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