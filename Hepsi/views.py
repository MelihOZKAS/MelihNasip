from django.shortcuts import render,HttpResponse,get_object_or_404
from .models import  SiirMasal,HikayeKategorileri,MasalKategorileri
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET

def turkish_slugify(input):
    tr_map = {
        'ş':'s',
        'Ş':'S',
        'ı':'i',
        'İ':'i',
        'I':'i',
        'ğ':'g',
        'Ğ':'G',
        'ü':'u',
        'Ü':'U',
        'ö':'o',
        'Ö':'O',
        'Ç':'C',
        'ç':'c'
    }
    for key, value in tr_map.items():
        input = input.replace(key, value)
    return slugify(input)


# Create your views here.
def home(request):
    masal_banner = MasalKategorileri.objects.filter(Aktif=True, Banner=True).order_by('sirasi')
    hikaye_banner = HikayeKategorileri.objects.filter(Aktif=True, Banner=True).order_by('sirasi')

    SmallMasal = SiirMasal.objects.filter(aktif=True,status="Yayinda",small_banner=True,Model="Masal").order_by('?')[:8]
    SmallHikaye = SiirMasal.objects.filter(aktif=True,status="Yayinda",small_banner=True,Model="Hikaye").order_by('?')[:8]

    title = "Çocuk Masalları & Çocuk Hikayeleri"
    description = "Sitemizde çocuklar için en sevilen masalları ve hikayeleri bulabilirsiniz. Klasik masallardan, öğretici hikayelere kadar geniş bir yelpazede içerik sunuyoruz. Çocuğunuzun hayal dünyasını zenginleştirecek bu özenle seçilmiş masalları ve hikayeleri keşfedin."
    keywords = "Çocuk Masalları, Çocuk Hikayeleri, Eğitici Hikayeler, Klasik Masallar, Öğretici Masallar, Çocuklar için Masallar, Çocuklar için Hikayeler,Uyku masalları "


    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
        'masal_banner': masal_banner,
        'hikaye_banner': hikaye_banner,

        'SmallMasal': SmallMasal,
        'SmallHikaye': SmallHikaye,
    }
    return render(request, 'system/Hepsi/home.html', context)


@csrf_exempt
def oto_masalkategoriekle(request):
    # Eklemek istediğiniz öğelerin listesi
    masal_listesi = ['Peri Masalları','Hayvan Masalları', 'Prenses Masalları','Prens Masalları','Aile Masalları','Macera Masalları','Komik Masallar','Eğitici Masallar','Arkadaş Masalları','Uyku Masalları','Kardeşlik Masalları','İyilik Masalları','Keloğlan Masalları','Dini Masallar']

    for masal in masal_listesi:
        # Eğer bu masal zaten varsa, geç
        if MasalKategorileri.objects.filter(MasalKategoriAdi=masal).exists():
            continue

        # Yeni bir MasalKategorileri örneği oluştur
        yeni_masal = MasalKategorileri(MasalKategoriAdi=masal, MasalSlug=turkish_slugify(masal),Banner=True,Aktif=True)

        # Yeni masalı veritabanına kaydet
        yeni_masal.save()

    return HttpResponse('Masallar başarıyla eklendi.')

def oto_hikayekategoriekle(request):
    # Eklemek istediğiniz öğelerin listesi
    hikaye_listesi = ["Sevimli Canavar Hikayeleri","ingilizce Hikayeler","Dini Hikayeler","Doğa ve Çevre Önemi Hikayeleri","Dostluk Hikayeleri","Muhteşem Bilim Hikayeleri","Uzay Maceraları Hikayeleri","Gezi Maceraları Hikayeleri","Eğlenceli Yolculuk Hikayeleri","Hazine Avı Hikayeleri","Mutlu Aile Hikayeleri","Korkusuz Kahraman Hikayeleri","Sevimli Hayvan Hikayeleri","Sihirli Dünya Hikayeleri"]

    for hikaye in hikaye_listesi:
        # Eğer bu masal zaten varsa, geç
        if HikayeKategorileri.objects.filter(HikayeKategoriAdi=hikaye).exists():
            continue

        # Yeni bir MasalKategorileri örneği oluştur
        yeni_hikaye = HikayeKategorileri(HikayeKategoriAdi=hikaye, HikayeSlug=turkish_slugify(hikaye),Banner=True,Aktif=True)

        # Yeni masalı veritabanına kaydet
        yeni_hikaye.save()

    return HttpResponse('Hikayeler başarıyla eklendi.')





def masalAltKategori(request, alt_kategori_slug):
    alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug=alt_kategori_slug)
    icerik_list = SiirMasal.objects.filter(masalKategorisi=alt_kategori,aktif=True,status="Yayinda",Model="Masal")
    sayfa_adi = f"En Güzel {alt_kategori.MasalKategoriAdi}"
    sayfa_Turu = "Masal"

    paginator = Paginator(icerik_list, 10) # 10 içerik göstermek için
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    if page_number is None:
        title = f"{alt_kategori.Masal_Title}"
        description = f"{alt_kategori.Masal_meta_description}"
    else:
        title = f"{alt_kategori.Masal_Title} - {page_number}"
        description = f"{alt_kategori.Masal_meta_description} - Sayfa {page_number}"



    context = {
        'title': title,
        'description': description,
        'keywords': alt_kategori.Masal_keywords,
        'alt_kategori': alt_kategori,
        'icerik': icerik,
        'sayfa_adi': sayfa_adi,
        'sayfa_Turu': sayfa_Turu,
    }
    return render(request, 'system/Hepsi/detay.html', context)



def hikayeAltKategori(request,  alt_kategori_slug):
    alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug=alt_kategori_slug)
    icerik_list = SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda", Model="Hikaye")
    sayfa_adi = f"En Güzel {alt_kategori.HikayeKategoriAdi}"
    sayfa_Turu = "Hikaye"


    paginator = Paginator(icerik_list, 10) # 10 içerik göstermek için
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    if page_number is None:
        title = f"{alt_kategori.Hikaye_Title}"
        description = f"{alt_kategori.Hikaye_meta_description}"
    else:
        title = f"{alt_kategori.Hikaye_Title} - {page_number}"
        description = f"{alt_kategori.Hikaye_meta_description} - Sayfa {page_number}"



    context = {
        'title': title,
        'description': description,
        'keywords': alt_kategori.Hikaye_keywords,
        'alt_kategori': alt_kategori,
        'icerik': icerik,
        'sayfa_adi': sayfa_adi,
        'sayfa_Turu': sayfa_Turu,

    }
    return render(request, 'system/Hepsi/detay.html', context)









def Masallar(request):
    Tum_Masallar = MasalKategorileri.objects.filter(Aktif=True).order_by('sirasi')

    title = "En Çok Okunan Çocuk Masalları | Uyku Masalları"
    description = "En popüler çocuk masallarını keşfedin. Klasiklerden modern masallara kadar çeşitli masallarla çocuğunuzun hayal dünyasını genişletin."
    keywords = "Çocuk Masalları, Klasik Masallar, Modern Masallar, Çocuklar için Masallar, Eğitici Masallar, Öğretici Masallar, Uyku Masalları"
    sayfa_adiH1 = "Tüm Masal Kategorileri"
    sayfa_Turu = "Masal"


    context = {
        'sayfa_adi': sayfa_adiH1,
        'sayfa_Turu': sayfa_Turu,
        'title': title,
        'description': description,
        'keywords': keywords,
        'masal_banner': Tum_Masallar,
    }
    return render(request, 'system/Hepsi/masallar.html', context)

def Hikayeler(request):
    Tum_Hikayeler = HikayeKategorileri.objects.filter(Aktif=True).order_by('sirasi')

    title = "Çocuklar İçin Eğitici Hikayeler | Çocuk Hikayeleri"
    description = "Çocuklar için özenle seçilmiş ilham verici hikayeler. Bu eğlenceli ve öğretici hikayelerle çocuğunuzun okuma sevgisini ve hayal gücünü geliştirin."
    keywords = "Çocuk Hikayeleri, İlham Verici Hikayeler, Eğitici Hikayeler, Çocuklar için Hikayeler, Öğretici Hikayeler, ingilizce hikayeler, dini hikayeler"
    sayfa_adiH1 = "Tüm Hikaye Kategorileri"
    sayfa_Turu = "Hikaye"

    context = {
        'sayfa_adi': sayfa_adiH1,
        'sayfa_Turu': sayfa_Turu,
        'title': title,
        'description': description,
        'keywords': keywords,
        'masal_banner': Tum_Hikayeler,
    }
    return render(request, 'system/Hepsi/masallar.html', context)




def iletisim(request):
    context = {
        'title': "Çocuk Masalları Oku İletişim",
        'description': "Çocuk hiyakeleri ve Masalları sitemizin iletişim bölümüdür bizimle irtibata geçebilirisiniz.",
        'keywords': "Çocuk masalları, eğitici masallar, uyku masalları, ingilizce hikayeler, çocuk hikayeleri, çocuklara özel hikayeler, keloğlan masalları",

    }

    return render(request, 'system/Hepsi/iletisim.html', context)


def enderunMasal(request,masal_slug):
    EnDerun = get_object_or_404(SiirMasal, slug=masal_slug)
    EnDerun.okunma_sayisi += 1  # okunma sayısını artır
    EnDerun.save()  # değişiklikleri kaydet
    BaskaMasal = SiirMasal.objects.filter(aktif=True,status="Yayinda",Model="Masal").order_by('?').first()
    BaskaHikaye = SiirMasal.objects.filter(aktif=True,status="Yayinda",Model="Hikaye").order_by('?').first()

    context = {
        'EnDerun': EnDerun,
        'BaskaMasal': BaskaMasal,
        'BaskaHikaye': BaskaHikaye,
        'title': EnDerun.title,
        'description': EnDerun.meta_description,
        'keywords': EnDerun.keywords,
    }
    return render(request, 'system/Hepsi/enderun.html', context)


def enderunHikaye(request,hikaye_slug):
    EnDerun = get_object_or_404(SiirMasal, slug=hikaye_slug)
    EnDerun.okunma_sayisi += 1  # okunma sayısını artır
    EnDerun.save()  # değişiklikleri kaydet
    BaskaMasal = SiirMasal.objects.filter(aktif=True,status="Yayinda",Model="Masal").order_by('?').first()
    BaskaHikaye = SiirMasal.objects.filter(aktif=True,status="Yayinda",Model="Hikaye").order_by('?').first()



    context = {
        'EnDerun': EnDerun,
        'BaskaMasal': BaskaMasal,
        'BaskaHikaye': BaskaHikaye,
        'title': EnDerun.title,
        'description': EnDerun.meta_description,
        'keywords': EnDerun.keywords,

    }
    return render(request, 'system/Hepsi/enderun.html', context)



@require_GET
def robots_txt(request):
    return HttpResponse(robots_txt_content, content_type="text/plain")

robots_txt_content = """
User-agent: *
Allow: /
Sitemap: https://www.cocukmasallarioku.com/sitemap.xml
"""


