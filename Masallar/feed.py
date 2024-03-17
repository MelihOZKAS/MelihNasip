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


class SihirliDunyaHikayelerFeed(Feed):
    title = "Sihirli Dünya Hikayeleri"
    link = "/feeds/sihirli-dunya-hikayeleri/"
    description = "En son eklenen sihirli dünya hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="sihirli-dunya-hikayeleri")
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


class SevimliHayvanHikayelerFeed(Feed):
    title = "Sevimli Hayvan Hikayeleri"
    link = "/feeds/sevimli-hayvan-hikayeleri/"
    description = "En son eklenen sevimli hayvan hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="sevimli-hayvan-hikayeleri")
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


class KahramanHikayelerFeed(Feed):
    title = "Korkusuz Kahraman Hikayeleri"
    link = "/feeds/korkusuz-kahraman-hikayeleri/"
    description = "En son eklenen korkusux kahraman hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="korkusuz-kahraman-hikayeleri")
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

class AileHikayelerFeed(Feed):
    title = "Mutlu Aile Hikayeleri"
    link = "/feeds/mutlu-aile-hikayeleri/"
    description = "En son eklenen mutlu aile hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="mutlu-aile-hikayeleri")
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


class HazineHikayelerFeed(Feed):
    title = "Hazine Hikayeleri"
    link = "/feeds/hazine-avi-hikayeleri/"
    description = "En son eklenen hazine avı hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="hazine-avi-hikayeleri")
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


class YolculukHikayelerFeed(Feed):
    title = "Eğlenceli Yolculuk Hikayeleri"
    link = "/feeds/eglenceli-yolculuk-hikayeleri/"
    description = "En son eklenen eğlenceli yolculuk hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="eglenceli-yolculuk-hikayeleri")
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

class GezikHikayelerFeed(Feed):
    title = "Gezi Maceraları Hikayeleri"
    link = "/feeds/gezi-maceralari-hikayeleri/"
    description = "En son eklenen gezi maceraları hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="gezi-maceralari-hikayeleri")
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

class UzayHikayelerFeed(Feed):
    title = "Uzay Maceraları Hikayeleri"
    link = "/feeds/uzay-maceralari-hikayeleri/"
    description = "En son eklenen uzay maceraları hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="uzay-maceralari-hikayeleri")
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

class BilimHikayelerFeed(Feed):
    title = "Muhteşem Bilim Hikayeleri"
    link = "/feeds/muhtesem-bilim-hikayeleri/"
    description = "En son eklenen muhteşem bilim hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="muhtesem-bilim-hikayeleri")
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

class DostlukHikayelerFeed(Feed):
    title = "Muhteşem Dostluk Hikayeleri"
    link = "/feeds/dostluk-hikayeleri/"
    description = "En son eklenen muhteşem dostluk hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="dostluk-hikayeleri")
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


class CevreHikayelerFeed(Feed):
    title = "Doğa ve Çevre Önemi Hikayeleri"
    link = "/feeds/doga-ve-cevre-onemi-hikayeleri/"
    description = "En son eklenen doğa ve çevre önemi hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="doga-ve-cevre-onemi-hikayeleri")
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


class ingilizceHikayelerFeed(Feed):
    title = "ingilizce çocuk Hikayeleri"
    link = "/feeds/ingilizce-hikayeler/"
    description = "En son eklenen ingilizce çocuk hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="ingilizce-hikayeler")
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


class CanavarHikayelerFeed(Feed):
    title = "Sevimli Canavar Hikayeleri"
    link = "/feeds/sevimli-canavar-hikayeleri/"
    description = "En son eklenen sevimli canavar hikayeleri."

    def items(self):
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug="sevimli-canavar-hikayeleri")
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
