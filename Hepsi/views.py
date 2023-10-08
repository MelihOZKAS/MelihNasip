from django.shortcuts import render,HttpResponse,get_object_or_404,reverse
from .models import  SiirMasal,HikayeKategorileri,MasalKategorileri,iletisimmodel
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def create_unique_title_slug(title):
    slug = turkish_slugify(title)
    unique_slug = slug
    unique_title = title
    num = 1
    while SiirMasal.objects.filter(slug=unique_slug).exists() or SiirMasal.objects.filter(title=unique_title).exists():
        unique_slug = '{}-{}'.format(slug, num)
        unique_title = '{} {}'.format(title, num)
        num += 1
    return unique_title, unique_slug


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

    title = "Çocuk Masalları & Çocuklara Hikayeler"
    description = "Çocuk masalları ve çocuk hikayeleri sitemizde masal okuyabilir masal dinleyebilir, uyku masallarına bakabilirsiniz. Masallar, hikayeler hepsi eğitici sitemizde"
    keywords = "Çocuk Masalları, Çocuk Masalları Oku, Masallar, Masal Dinle, Kısa Masallar, Masal Oku, Masallar, Çocuk Hikayeleri, Eğitici Hikayeler, Klasik Masallar, Öğretici Masallar, Çocuklar için Masallar, Çocuklar için Hikayeler,Uyku masalları"


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
    icerik_list = SiirMasal.objects.filter(masalKategorisi=alt_kategori,aktif=True,status="Yayinda",Model="Masal").order_by('-olusturma_tarihi')
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
    return render(request, 'system/Hepsi/detay-yeni.html', context)



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
    return render(request, 'system/Hepsi/detay-yeni.html', context)









def Masallar(request):
    Tum_Masallar = MasalKategorileri.objects.filter(Aktif=True).order_by('sirasi')

    title = "Çocuk Masallı, Çocuklara Uyku Masalları | Masal Oku"
    description = "En çok okunan masalları keşfedin. Çocuklara özel eğitici öğretici uyku masalı ve fazlası için masal sitemizi takip edin. En güzel masallar"
    keywords = "Çocuk Masalları, Klasik Masallar, Modern Masallar, Çocuklar için Masallar, Masal Oku, Masal Dinle, Masal Dinle, Eğitici Masallar, Öğretici Masallar, Uyku Masalları"
    sayfa_adiH1 = "Masallar Oku: Çocuklar İçin Eğitici Uyku Masalları, Kısa Hikayeler ve Daha Fazlası"
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

    title = "Çocuklar için Eğitici Hikayeler | Çocuk Hikayeleri"
    description = "Çocuklar için özenle seçilmiş ilham verici hikayeler. Bu eğlenceli ve öğretici hikayelerle çocuğunuzun okuma sevgisini ve hayal gücünü geliştirin."
    keywords = "Çocuk Hikayeleri, Hikaye, Hikayeler, İlham Verici Hikayeler, Eğitici Hikayeler, Çocuklar için Hikayeler, Öğretici Hikayeler, ingilizce hikayeler, Dini hikayeler, Uyku hikayeleri, Hikaye dinle"
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






def ekle(request):
    context = {
        'title': "Uyku Masalları, Uyku Hikayeleri Ekle",
        'description': "Çocuk hiyakeleri ve Masallarını bizlere gönderebilir sizin yazdıklarınızı da bizlerle ve tüm türkiye ile paylaşabilirisiniz.",
        'keywords': "çocuk masalları yaz, uyku masalları yaz, uyku hikayeleri yaz, çocuk hikayeleri yaz, uzun çocuklara özel hikaye,zeka geliştirin hikayeler",

    }
    if request.method == 'POST':
        title = request.POST.get('title')
        model = request.POST.get('model')
        icerik = request.POST.get('icerik')
        aciklama = request.POST.get('aciklama')

        icerik = icerik.replace('\n', '<br>')

        title, slug = create_unique_title_slug(title)
        siir_masal = SiirMasal(title=title, Model=model, icerik=icerik, slug=slug, meta_description=aciklama , status="manuel")
        siir_masal.save()
        # Burada başka bir sayfaya yönlendirme yapabilirsiniz.
        return HttpResponse('Ellerinize Sağlık Yazdığınız içeriği Kaydettik Kontrollerden Sonra Yayınlanacaktır. <a href="{}" class="btn btn-primary">Yeni masal/hikaye eklemek için tıklayınız.</a>'.format(reverse('masal-hikaye-ekle')))


    else:
        return render(request, 'system/Hepsi/masal-ekle.html',context)  # Formun bulunduğu sayfa



def iletisim(request):
    context = {
        'title': "Uyku Çocuk Masallarını Dinle - İletişim Sayfası | Masal Oku",
        'description': "Çocuk hiyakeleri ve Çocuk Masalları sitemizin iletişim bölümüdür bizimle irtibata geçebilirisiniz. Masal okuya bilir gönderebilir siniz.",
        'keywords': "Çocuk masalları, eğitici masallar, uyku masalları, ingilizce hikayeler, çocuk hikayeleri, çocuklara özel hikayeler, keloğlan masalları",

    }

    if request.method == 'POST':
        name = request.POST.get('InputName')
        email = request.POST.get('InputEmail')
        title = request.POST.get('InputSubject')
        icerik = request.POST.get('InputMessage')

        iletisim_obj = iletisimmodel(name=name, email=email, title=title, icerik=icerik)
        iletisim_obj.save()

        return HttpResponse('İletişim istediğinizi Kaydettik. <a href="{}" class="btn btn-primary">Ana Sayfaya Dönmek için Tıklayın.</a>'.format(reverse('home')))


    return render(request, 'system/Hepsi/iletisim.html', context)

def hakkimizda(request):
    context = {
        'title': "Uyku Çocuk Hikayeleri Dinle - Hakkımızda | Hikaye Oku",
        'description': "Çocuk hiyakeleri ve Masalları sitemizin hakkımızda bölümüdür. Masal ve Hikayeler için iletişime geçebilirsiniz.",
        'keywords': "Çocuk masalları, eğitici masallar, uyku masalları, uzun uyku hikayeleri, çocuk hikayeleri, uyku getiren masallar, keloğlan masalları",

    }

    return render(request, 'system/Hepsi/hakkimizda.html', context)

def gizlilik(request):
    context = {
        'title': "Çocuk Hikayeleri ve Masalları Oku - Gizlilik Politikası",
        'description': "Çocuk hiyakeleri ve Masalları sitemizin Gizlilik Politikası bölümüdür. Masal ve Hikayeler için iletişime geçebilirsiniz.",
        'keywords': "Çocuk masalları, eğitici masallar, uyku masalları, uzun uyku hikayeleri, en güzel çocuk hikayeleri, uyku getiren masallar, keloğlan masalları",

    }

    return render(request, 'system/Hepsi/gilzlilik.html', context)

def kullanim(request):
    context = {
        'title': "Çocuk Masallarını Dinle - Kullanım Şartları | Masal Oku",
        'description': "Çocuk hiyakeleri ve Masalları sitemizin Kullanım Şartları bölümüdür. Masal ve Hikayeler için iletişime geçebilirsiniz.",
        'keywords': "Çocuk masalları, eğitici masallar, uyku masalları, uzun uyku hikayeleri, keloğlan masalları, en güzel çocuk hikayeleri, uyku getiren masallar, keloğlan masalları",

    }

    return render(request, 'system/Hepsi/kullanim.html', context)

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


def Oto_Paylas(request):
    post = SiirMasal.objects.filter(status="oto").order_by('id').first()

    if post is not None:
        if post.yayin_tarihi is None or post.yayin_tarihi <= timezone.now():
            post.status = "Yayinda"
            post.aktif = True
            post.save()
            return HttpResponse(f'Şükürler Olsun "{post.title}" Paylaşıldı.')
    else:
        return HttpResponse('Paylaşılacak Post Bulunamadı.')