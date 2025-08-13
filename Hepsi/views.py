from django.shortcuts import render, HttpResponse, get_object_or_404, reverse
from .models import SiirMasal, HikayeKategorileri, MasalKategorileri, iletisimmodel, Blog, Animals, Oyunlar, MobileUser, FavoriteStory
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.utils import IntegrityError
import re
from django.db.models import Q, F
import random

from html import unescape
from django.http import JsonResponse
from django.utils.html import strip_tags
from django.utils.encoding import smart_str, force_str
import html
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseBadRequest, \
    HttpResponseServerError
import json




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
        'ş': 's',
        'Ş': 'S',
        'ı': 'i',
        'İ': 'i',
        'I': 'i',
        'ğ': 'g',
        'Ğ': 'G',
        'ü': 'u',
        'Ü': 'U',
        'ö': 'o',
        'Ö': 'O',
        'Ç': 'C',
        'ç': 'c'
    }
    for key, value in tr_map.items():
        input = input.replace(key, value)
    return slugify(input)


def get_youtube_id(url):
    # YouTube video URL'sinden video ID'sini çıkaran bir regex deseni
    link = url.replace("https://www.youtube.com/embed/", "")
    youtube_id = link.split("?")
    return youtube_id[0] if youtube_id else None


# Create your views here.
def home(request):
    cache_key = 'home_context'
    context = cache.get(cache_key)

    if context is None:
        masal_banner = MasalKategorileri.objects.filter(Aktif=True, Banner=True).order_by('sirasi')
        hikaye_banner = HikayeKategorileri.objects.filter(Aktif=True, Banner=True).order_by('sirasi')

        title = "Çocuk Masalları | Uyku Masalı | Çocuk Hikayeleri | Masal Oku"
        description = "Çocuklar için en güzel masallar, Uyku masalları, hayvan masalları, klasik masallar. Çocuğunuzun hayal gücünü geliştirecek masallarımızı keşfedin masal oku"
        keywords = "Çocuk Masalları, Çocuk Masalları Oku, Masallar, Masal Dinle, Kısa Masallar, Masal Oku, Masallar, Çocuk Hikayeleri, Eğitici Hikayeler, Klasik Masallar, Öğretici Masallar, Çocuklar için Masallar, Çocuklar için Hikayeler,Uyku masalları"

        context = {
            'title': title,
            'description': description,
            'keywords': keywords,
            'masal_banner': masal_banner,
            'hikaye_banner': hikaye_banner,
        }
        cache.set(cache_key, context, 60 * 60 * 2)

    return render(request, 'system/Hepsi/home.html', context)


@csrf_exempt
def oto_masalkategoriekle(request):
    # Eklemek istediğiniz öğelerin listesi
    masal_listesi = ['Peri Masalları', 'Hayvan Masalları', 'Prenses Masalları', 'Prens Masalları', 'Aile Masalları',
                     'Macera Masalları', 'Komik Masallar', 'Eğitici Masallar', 'Arkadaş Masalları', 'Uyku Masalları',
                     'Kardeşlik Masalları', 'İyilik Masalları', 'Keloğlan Masalları', 'Dini Masallar']

    for masal in masal_listesi:
        # Eğer bu masal zaten varsa, geç
        if MasalKategorileri.objects.filter(MasalKategoriAdi=masal).exists():
            continue

        # Yeni bir MasalKategorileri örneği oluştur
        yeni_masal = MasalKategorileri(MasalKategoriAdi=masal, MasalSlug=turkish_slugify(masal), Banner=True,
                                       Aktif=True)

        # Yeni masalı veritabanına kaydet
        yeni_masal.save()

    return HttpResponse('Masallar başarıyla eklendi.')


def oto_hikayekategoriekle(request):
    # Eklemek istediğiniz öğelerin listesi
    hikaye_listesi = ["Sevimli Canavar Hikayeleri", "ingilizce Hikayeler", "Dini Hikayeler",
                      "Doğa ve Çevre Önemi Hikayeleri", "Dostluk Hikayeleri", "Muhteşem Bilim Hikayeleri",
                      "Uzay Maceraları Hikayeleri", "Gezi Maceraları Hikayeleri", "Eğlenceli Yolculuk Hikayeleri",
                      "Hazine Avı Hikayeleri", "Mutlu Aile Hikayeleri", "Korkusuz Kahraman Hikayeleri",
                      "Sevimli Hayvan Hikayeleri", "Sihirli Dünya Hikayeleri"]

    for hikaye in hikaye_listesi:
        # Eğer bu masal zaten varsa, geç
        if HikayeKategorileri.objects.filter(HikayeKategoriAdi=hikaye).exists():
            continue

        # Yeni bir MasalKategorileri örneği oluştur
        yeni_hikaye = HikayeKategorileri(HikayeKategoriAdi=hikaye, HikayeSlug=turkish_slugify(hikaye), Banner=True,
                                         Aktif=True)

        # Yeni masalı veritabanına kaydet
        yeni_hikaye.save()

    return HttpResponse('Hikayeler başarıyla eklendi.')


def masalAltKategori(request, alt_kategori_slug):
    page_number = request.GET.get('sayfa') or '1'
    cache_key = f'masal_alt_{alt_kategori_slug}_p_{page_number}'
    context = cache.get(cache_key)

    if context is None:
        alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug=alt_kategori_slug)
        icerik_list = SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                               Model="Masal").order_by('-guncelleme_tarihi')
        sayfa_adi = f"En Güzel {alt_kategori.MasalKategoriAdi}"
        sayfa_Turu = "Masal"

        paginator = Paginator(icerik_list, 10)
        icerik = paginator.get_page(page_number)

        if page_number in [None, '1']:
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
        cache.set(cache_key, context, 60 * 60 * 2)

    return render(request, 'system/Hepsi/detay-yeni.html', context)


def MasalOkuListesi(request):
    page_number = request.GET.get('sayfa') or '1'
    cache_key = f'masal_list_p_{page_number}'
    context = cache.get(cache_key)

    if context is None:
        icerik_list = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('-guncelleme_tarihi')[:250]
        sayfa_adi = f"Çocuklara Uyku Öncesi Masal Oku"
        sayfa_Turu = "Masal"

        paginator = Paginator(icerik_list, 14)
        icerik = paginator.get_page(page_number)

        base_title = "Çocuk Masalları | Uyku Masalları | Kısa Masal | Masal Oku"
        base_description = "Çocuklarınızın hayal dünyasını genişletmek ve onlara keyifli anlar yaşatmak için Masal Oku sayfamızı ziyaret edin. Uyku öncesi masallar ve kısa masal oku"
        Keys = "Masal Oku, Çocuk Masalları, Eğitici Masallar, Eğlenceli Masallar, Öğretici Masallar, Fantastik Masallar, İlgi Çekici Masallar, En İyi Masallar, En Güzel Masallar, Popüler Masallar"

        if page_number in [None, '1']:
            title = base_title
            description = base_description
        else:
            title = f"{base_title} - {page_number}"
            description = f"{base_description} - Sayfa {page_number}"

        context = {
            'title': title,
            'description': description,
            'keywords': Keys,
            'alt_kategori': "YOKKKKKK",
            'icerik': icerik,
            'sayfa_adi': sayfa_adi,
            'sayfa_Turu': sayfa_Turu,
        }
        cache.set(cache_key, context, 60 * 60 * 2)

    return render(request, 'system/Hepsi/oku-url-detay-yeni.html', context)


def hikayeAltKategori(request, alt_kategori_slug):
    page_number = request.GET.get('sayfa') or '1'
    cache_key = f'hikaye_alt_{alt_kategori_slug}_p_{page_number}'
    context = cache.get(cache_key)

    if context is None:
        alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug=alt_kategori_slug)
        icerik_list = SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                               Model="Hikaye").order_by('-guncelleme_tarihi')
        sayfa_adi = f"En Güzel {alt_kategori.HikayeKategoriAdi}"
        sayfa_Turu = "Hikaye"

        paginator = Paginator(icerik_list, 10)
        icerik = paginator.get_page(page_number)

        if page_number in [None, '1']:
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
        cache.set(cache_key, context, 60 * 60 * 2)

    return render(request, 'system/Hepsi/detay-yeni.html', context)


def hikayeOkuListesi(request):
    page_number = request.GET.get('sayfa') or '1'
    cache_key = f'hikaye_list_p_{page_number}'
    context = cache.get(cache_key)

    if context is None:
        icerik_list = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by('-guncelleme_tarihi')[:50]
        sayfa_adi = f"En Güzel Çocuk Hikayeleri Oku"
        sayfa_Turu = "Hikaye"

        paginator = Paginator(icerik_list, 10)
        icerik = paginator.get_page(page_number)

        base_title = "Aile Hikayeleri, Dini Hikaye En Güzel Hikayeler | Hikaye Oku"
        base_description = "Çocuklarınızın hayal dünyasını genişletmek ve onlara keyifli anlar yaşatmak için Hikaye Oku sayfamızı ziyaret edin. Çocuklara özel  uzun hikaye oku ve dinle"
        Keys = "Hikaye Oku, Çocuk Hikayeleri, Eğitici Hikayeleri, Eğlenceli Hikayeleri, Öğretici Hikayeleri, Fantastik Hikayeleri, ingilizce Hikayeler, En İyi hikayeler, En Güzel Hikayeler, Popüler Hikayeler"

        if page_number in [None, '1']:
            title = base_title
            description = base_description
        else:
            title = f"{base_title} - {page_number}"
            description = f"{base_description} - Sayfa {page_number}"

        context = {
            'title': title,
            'description': description,
            'keywords': Keys,
            'alt_kategori': "YOKKKKKK",
            'icerik': icerik,
            'sayfa_adi': sayfa_adi,
            'sayfa_Turu': sayfa_Turu,
        }
        cache.set(cache_key, context, 60 * 60 * 2)

    return render(request, 'system/Hepsi/oku-url-detay-yeni.html', context)


def BlogHome(request):
    page_number = request.GET.get('sayfa') or '1'
    section = request.resolver_match.url_name or 'blog'
    cache_key = f'blog_home_{section}_p_{page_number}'
    context = cache.get(cache_key)

    if context is None:
        if section == 'cocuk':
            icerik_list = Blog.objects.filter(aktif=True, status="Yayinda", Model="cocuk").order_by('-olusturma_tarihi')
            keywords = "Çocuk Gelişimi, Fiziksel Gelişim, Duygusal Gelişim, Zihinsel Gelişim, Çocuk Psikolojisi, Ebeveynlik İpuçları, çocuk gelişimi kitapları, çocuk gelişimi masalları, çocuk gelişimi hikayeleri",
            sayfa_adi = f"Çocuk Gelişimi Bilimsel Araştırmalarla Desteklenen Pratik Bilgiler"
            title = f"Çocuk Gelişimi Araştırmalar ve Pratik Bilgi | Masal Oku"
            description = f"Çocuk gelişimindeki en son bilimsel bulguları ve pratik bilgiler. Çocuğunuzun fiziksel, duygusal ve zihinsel gelişimini destekler."
        elif section == 'saglik':
            icerik_list = Blog.objects.filter(aktif=True, status="Yayinda", Model="saglik").order_by('-olusturma_tarihi')
            keywords = "Çocuk Gelişimi, Fiziksel Gelişim, Duygusal Gelişim, Zihinsel Gelişim, Çocuk Psikolojisi, Ebeveynlik İpuçları, çocuk gelişimi kitapları, çocuk gelişimi masalları, çocuk gelişimi hikayeleri",
            sayfa_adi = f"Çocuk Gelişimi Bilimsel Araştırmalarla Desteklenen Pratik Bilgiler"
            title = f"Çocuk Gelişimi Araştırmalar ve Pratik Bilgi | Masal Oku"
            description = f"Çocuk gelişimindeki en son bilimsel bulguları ve pratik bilgiler. Çocuğunuzun fiziksel, duygusal ve zihinsel gelişimini destekler."
        elif section == 'kadin':
            icerik_list = Blog.objects.filter(aktif=True, status="Yayinda", Model="kadin").order_by('-olusturma_tarihi')
            keywords = "Çocuk Gelişimi, Fiziksel Gelişim, Duygusal Gelişim, Zihinsel Gelişim, Çocuk Psikolojisi, Ebeveynlik İpuçları, çocuk gelişimi kitapları, çocuk gelişimi masalları, çocuk gelişimi hikayeleri",
            sayfa_adi = f"Çocuk Gelişimi Bilimsel Araştırmalarla Desteklenen Pratik Bilgiler"
            title = f"Çocuk Gelişimi Araştırmalar ve Pratik Bilgi | Masal Oku"
            description = f"Çocuk gelişimindeki en son bilimsel bulguları ve pratik bilgiler. Çocuğunuzun fiziksel, duygusal ve zihinsel gelişimini destekler."
        else:
            icerik_list = Blog.objects.filter(aktif=True, status="Yayinda").order_by('-olusturma_tarihi')
            keywords = ""
            sayfa_adi = "Blog"
            title = "Blog | Masal Oku"
            description = "Çocuk gelişimi ve ebeveynlik hakkında yazılar"

        paginator = Paginator(icerik_list, 10)
        icerik = paginator.get_page(page_number)

        if page_number in [None, '1']:
            title = title
            description = description
        else:
            title = f"{title} - {page_number}"
            description = f"{description} - Sayfa {page_number}"

        context = {
            'title': title,
            'description': description,
            'keywords': keywords,
            'icerik': icerik,
            'sayfa_adi': sayfa_adi,
        }
        cache.set(cache_key, context, 60 * 60)

    return render(request, 'system/Hepsi/bloghome.html', context)


@vary_on_headers("Accept-Language")
@cache_page(60 * 60 * 2)
def Masallar(request):
    Tum_Masallar = MasalKategorileri.objects.filter(Aktif=True).order_by('sirasi')

    title = "Çocuk Masalları, Çocuklara Uyku Masalları | Masal Oku"
    description = "En çok okunan masalları keşfedin. Çocuklara özel eğitici öğretici uyku masalı ve fazlası için masal sitemizi takip edin. En güzel masallar"
    keywords = "Çocuk Masalları, Klasik Masallar, Modern Masallar, Çocuklar için Masallar, Masal Oku, Masal Dinle, Masal Dinle, Eğitici Masallar, Öğretici Masallar, Uyku Masalları"
    sayfa_adiH1 = "Çocuk Masalları, Eğitici Masallar, Kısa Masallar ve Uyku Masalları Oku"
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


@vary_on_headers("Accept-Language")
@cache_page(60 * 60 * 2)
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
        siir_masal = SiirMasal(title=title, Model=model, icerik=icerik, slug=slug, meta_description=aciklama,
                               status="manuel")
        siir_masal.save()
        # Burada başka bir sayfaya yönlendirme yapabilirsiniz.
        return HttpResponse(
            'Ellerinize Sağlık Yazdığınız içeriği Kaydettik Kontrollerden Sonra Yayınlanacaktır. <a href="{}" class="btn btn-primary">Yeni masal/hikaye eklemek için tıklayınız.</a>'.format(
                reverse('masal-hikaye-ekle')))


    else:
        return render(request, 'system/Hepsi/masal-ekle.html', context)  # Formun bulunduğu sayfa


def iletisim(request):
    if request.method == 'POST':
        name = request.POST.get('InputName')
        email = request.POST.get('InputEmail')
        title = request.POST.get('InputSubject')
        icerik = request.POST.get('InputMessage')

        iletisim_obj = iletisimmodel(name=name, email=email, title=title, icerik=icerik)
        iletisim_obj.save()

        return HttpResponse(
            'İletişim istediğinizi Kaydettik. <a href="{}" class="btn btn-primary">Ana Sayfaya Dönmek için Tıklayın.</a>'.format(
                reverse('home')))

    cache_key = 'iletisim_context'
    context = cache.get(cache_key)
    if context is None:
        context = {
            'title': "İletişim | Çocuk Masalları ve Hikayeleri | Masal Oku",
            'description': "Sorularınız, önerileriniz ve iş birlikleri için bizimle iletişime geçin. Çocuk masalları ve hikayeleri hakkında her konuda hızlı dönüş yapıyoruz.",
            'keywords': "iletişim, masal iletişim, çocuk masalları iletişim, hikaye iletişim, destek, öneri, iş birliği",
        }
        cache.set(cache_key, context, 60 * 60 * 12)

    return render(request, 'system/Hepsi/iletisim.html', context)


def hakkimizda(request):
    cache_key = 'hakkimizda_context'
    context = cache.get(cache_key)
    if context is None:
        context = {
            'title': "Hakkımızda | Çocuk Masalları ve Hikayeleri | Masal Oku",
            'description': "Çocuklara güvenli, eğitici ve ücretsiz masal-hikaye deneyimi sunuyoruz. Aileler için kaliteli içerikleri özenle seçip düzenli olarak yayınlıyoruz.",
            'keywords': "hakkımızda, çocuk masalları, çocuk hikayeleri, eğitici içerik, aile dostu, ücretsiz masal",
        }
        cache.set(cache_key, context, 60 * 60 * 12)

    return render(request, 'system/Hepsi/hakkimizda.html', context)


def gizlilik(request):
    cache_key = 'gizlilik_context'
    context = cache.get(cache_key)
    if context is None:
        context = {
            'title': "Gizlilik Politikası | Çocuk Masalları ve Hikayeleri",
            'description': "Kişisel verilerin korunması, çerez kullanımı ve üçüncü taraf hizmetleri hakkında tüm detaylar. Çocukların gizliliğini önceliklendiriyoruz.",
            'keywords': "gizlilik politikası, KVKK, çerezler, kişisel veriler, veri güvenliği, çocuk güvenliği",
        }
        cache.set(cache_key, context, 60 * 60 * 12)

    return render(request, 'system/Hepsi/eski-gilzlilik.html', context)


def cerez(request):
    cache_key = 'cerez_context'
    context = cache.get(cache_key)
    if context is None:
        context = {
            'title': "Çerez Politikası | Çocuk Masalları ve Hikayeleri",
            'description': "Hangi çerezleri neden kullandığımızı, tercihlerinizi nasıl yönetebileceğinizi ve çerezleri nasıl devre dışı bırakabileceğinizi öğrenin.",
            'keywords': "çerez politikası, cookie policy, çerez türleri, çerez ayarları, takip teknolojileri",
        }
        cache.set(cache_key, context, 60 * 60 * 12)

    return render(request, 'system/Hepsi/cerez.html', context)


def kullanim(request):
    cache_key = 'kullanim_context'
    context = cache.get(cache_key)
    if context is None:
        context = {
            'title': "Kullanım Şartları | Çocuk Masalları ve Hikayeleri",
            'description': "Site kullanım koşulları, telif hakları ve sorumluluk reddi hakkında bilgi alın. Güvenli ve şeffaf kullanım ilkeleri.",
            'keywords': "kullanım şartları, telif, sorumluluk reddi, kullanıcı sözleşmesi, koşullar",
        }
        cache.set(cache_key, context, 60 * 60 * 12)

    return render(request, 'system/Hepsi/kullanim.html', context)


def enderunMasal(request, masal_slug):
    cache_key = f'enderun_masal_context_{masal_slug}'
    context = cache.get(cache_key)

    if context is None:
        EnDerun = get_object_or_404(SiirMasal, Model="Masal", slug=masal_slug, aktif=True, status="Yayinda")

        BaskaMasal = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('?').first()
        BaskaHikaye = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by('?').first()

        thumbnail_url = None
        if EnDerun.youtube:
            youtube_id = get_youtube_id(EnDerun.youtube)
            thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/0.jpg"

        if EnDerun.Model == 'Masal':
            categories = EnDerun.masalKategorisi.all()
            category_names = [category.MasalKategoriAdi for category in categories]
        elif EnDerun.Model == 'Hikaye':
            categories = EnDerun.hikayeKategorisi.all()
            category_names = [category.HikayeKategoriAdi for category in categories]
        else:
            categories = []
            category_names = []

        category_names_str = ', '.join(category_names) if category_names else EnDerun.Model

        content_fields = ['icerik'] + [f'icerik{n}' for n in range(2, 11)]
        contents = [getattr(EnDerun, field, None) for field in content_fields]
        articleBody = ' '.join([c for c in contents if c])

        resimler = []
        if EnDerun.resim:
            resimler.append(EnDerun.resim.url)
        if EnDerun.resim2:
            resimler.append(EnDerun.resim2.url)
        if EnDerun.resim3:
            resimler.append(EnDerun.resim3.url)
        if EnDerun.resim4:
            resimler.append(EnDerun.resim4.url)
        if EnDerun.resim5:
            resimler.append(EnDerun.resim5.url)
        if EnDerun.resim6:
            resimler.append(EnDerun.resim6.url)
        if EnDerun.resim7:
            resimler.append(EnDerun.resim7.url)
        if EnDerun.resim8:
            resimler.append(EnDerun.resim8.url)
        if EnDerun.resim9:
            resimler.append(EnDerun.resim9.url)
        if EnDerun.resim10:
            resimler.append(EnDerun.resim10.url)
        if not resimler:
            resimler.append("https://masalbucket.s3.amazonaws.com/static/images/Masal-Oku-Hikaye-Oku.webp")

        context = {
            'EnDerun': EnDerun,
            'BaskaMasal': BaskaMasal,
            'BaskaHikaye': BaskaHikaye,
            'title': EnDerun.title,
            'description': EnDerun.meta_description,
            'keywords': EnDerun.keywords,
            'TumKategori': category_names_str,
            'thumbnail_url': thumbnail_url,
            'resimler': resimler,
            'articleBody': articleBody,
        }
        cache.set(cache_key, context, 60 * 60 * 2)  # 2 saat cache

    return render(request, 'system/Hepsi/enderun.html', context)


def enderunBlog(request, blog_slug):
    cache_key = f'enderun_blog_context_{blog_slug}'
    context = cache.get(cache_key)

    if context is None:
        EnDerun = get_object_or_404(Blog, slug=blog_slug, aktif=True, status="Yayinda")
        BaskaMasal = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('?').first()
        BaskaHikaye = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by('?').first()
        category_names_str = "Çocuk Gelişimi"

        thumbnail_url = None
        if EnDerun.youtube:
            youtube_id = get_youtube_id(EnDerun.youtube)
            thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/0.jpg"

        content_fields = ['icerik'] + [f'icerik{n}' for n in range(1, 11)]
        contents = [getattr(EnDerun, field, None) for field in content_fields]
        articleBody = ' '.join([c for c in contents if c])

        resimler = []
        if EnDerun.resim:
            resimler.append(EnDerun.resim.url)
        if EnDerun.resim2:
            resimler.append(EnDerun.resim2.url)
        if EnDerun.resim3:
            resimler.append(EnDerun.resim3.url)
        if EnDerun.resim4:
            resimler.append(EnDerun.resim4.url)
        if not resimler:
            resimler.append("https://masalbucket.s3.amazonaws.com/static/images/Masal-Oku-Hikaye-Oku.webp")

        context = {
            'EnDerun': EnDerun,
            'BaskaMasal': BaskaMasal,
            'BaskaHikaye': BaskaHikaye,
            'title': EnDerun.title,
            'description': EnDerun.meta_description,
            'keywords': EnDerun.keywords,
            'TumKategori': category_names_str,
            'thumbnail_url': thumbnail_url,
            'resimler': resimler,
            'articleBody': articleBody,
        }
        cache.set(cache_key, context, 60 * 60 * 2)

    return render(request, 'system/Hepsi/blog-Enderun.html', context)


def enderunHikaye(request, hikaye_slug):
    cache_key = f'enderun_hikaye_context_{hikaye_slug}'
    context = cache.get(cache_key)

    if context is None:
        EnDerun = get_object_or_404(SiirMasal, Model="Hikaye", slug=hikaye_slug, aktif=True, status="Yayinda")

        BaskaMasal = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('?').first()
        BaskaHikaye = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by('?').first()

        thumbnail_url = None
        if EnDerun.youtube:
            youtube_id = get_youtube_id(EnDerun.youtube)
            thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/0.jpg"

        if EnDerun.Model == 'Masal':
            categories = EnDerun.masalKategorisi.all()
            category_names = [category.MasalKategoriAdi for category in categories]
        elif EnDerun.Model == 'Hikaye':
            categories = EnDerun.hikayeKategorisi.all()
            category_names = [category.HikayeKategoriAdi for category in categories]
        else:
            categories = []
            category_names = []

        category_names_str = ', '.join(category_names) if category_names else EnDerun.Model

        content_fields = ['icerik'] + [f'icerik{n}' for n in range(2, 11)]
        contents = [getattr(EnDerun, field, None) for field in content_fields]
        articleBody = ' '.join([c for c in contents if c])

        resimler = []
        if EnDerun.resim:
            resimler.append(EnDerun.resim.url)
        if EnDerun.resim2:
            resimler.append(EnDerun.resim2.url)
        if EnDerun.resim3:
            resimler.append(EnDerun.resim3.url)
        if EnDerun.resim4:
            resimler.append(EnDerun.resim4.url)
        if EnDerun.resim5:
            resimler.append(EnDerun.resim5.url)
        if EnDerun.resim6:
            resimler.append(EnDerun.resim6.url)
        if EnDerun.resim7:
            resimler.append(EnDerun.resim7.url)
        if EnDerun.resim8:
            resimler.append(EnDerun.resim8.url)
        if EnDerun.resim9:
            resimler.append(EnDerun.resim9.url)
        if EnDerun.resim10:
            resimler.append(EnDerun.resim10.url)
        if not resimler:
            resimler.append("https://masalbucket.s3.amazonaws.com/static/images/Masal-Oku-Hikaye-Oku.webp")

        context = {
            'EnDerun': EnDerun,
            'BaskaMasal': BaskaMasal,
            'BaskaHikaye': BaskaHikaye,
            'title': EnDerun.title,
            'description': EnDerun.meta_description,
            'keywords': EnDerun.keywords,
            'TumKategori': category_names_str,
            'thumbnail_url': thumbnail_url,
            'resimler': resimler,
            'articleBody': articleBody,
        }
        cache.set(cache_key, context, 60 * 60 * 2)

    return render(request, 'system/Hepsi/enderun.html', context)


@require_GET
def robots_txt(request):
    return HttpResponse(robots_txt_content, content_type="text/plain")


robots_txt_content = """
User-agent: *
Disallow: /static/
Allow: /media/
Sitemap: https://www.cocukmasallarioku.com/sitemap.xml

Disallow: /feeds/
"""


@require_GET
def ads(request):
    return HttpResponse(ads_content, content_type="text/plain")


ads_content = """google.com, pub-7065951693101615, DIRECT, f08c47fec0942fa0"""


def Oto_Paylas(request):
    post = SiirMasal.objects.filter(status="oto").order_by('id').first()

    if post is not None:
        if post.yayin_tarihi is None or post.yayin_tarihi <= timezone.now():
            post.status = "Yayinda"
            post.resimText = ""
            post.aktif = True
            post.indexing = True  # indekslendi olarak işaretle
            post.olusturma_tarihi = timezone.now()  # eklenme tarihini güncelle
            post.save()
            return HttpResponse(f'Şükürler Olsun "{post.title}" Paylaşıldı.')
    else:
        return HttpResponse('Paylaşılacak Post Bulunamadı.')


def Blog_oto_Paylas(request):
    post = Blog.objects.filter(status="oto").order_by('id').first()

    if post is not None:
        if post.yayin_tarihi is None or post.yayin_tarihi <= timezone.now():
            post.status = "Yayinda"
            post.aktif = True
            # post.indexing = True  # indekslendi olarak işaretle
            post.olusturma_tarihi = timezone.now()  # eklenme tarihini güncelle
            post.save()
            return HttpResponse(f'Şükürler Olsun "{post.title}" Paylaşıldı.')
    else:
        return HttpResponse('Paylaşılacak Post Bulunamadı.')


@csrf_exempt
def apiyle_ekle(request):
    if request.method == 'POST':
        # Gelen POST isteğindeki değerleri alın
        title = request.POST.get('title')
        icerik = request.POST.get('icerik')
        model = request.POST.get('model')
        key = request.POST.get('kew')

        title, slug = create_unique_title_slug(title)
        siir_masal = SiirMasal(title=title, Model=model, icerik=icerik, slug=slug, keywords=key, status="Taslak")
        siir_masal.save()
        if siir_masal.id is None:
            return HttpResponse("Model kaydedilemedi.")
        else:
            return HttpResponse("Model başarıyla kaydedildi. ID: " + str(siir_masal.id))


@csrf_exempt
def indexing_var_mi(request):
    post = SiirMasal.objects.filter(indexing=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un indexing durumunu False yapayı unutmamak lazımmm dimi.
        post.indexing = False
        post.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinterest'])
        return HttpResponse(
            f"https://www.cocukmasallarioku.com/{'masal-oku' if post.Model == 'Masal' else 'hikaye-oku'}/{post.slug}/")
    else:
        return HttpResponse("post bulunamadı.")


@csrf_exempt
def blog_indexing_var_mi(request):
    post = Blog.objects.filter(indexing=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un indexing durumunu False yapayı unutmamak lazımmm dimi.
        post.indexing = False
        post.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinterest'])
        return HttpResponse(
            f"https://www.cocukmasallarioku.com/{post.slug}/")
    else:
        return HttpResponse("post bulunamadı.")


@csrf_exempt
def facebook_var_mi(request):
    post = SiirMasal.objects.filter(facebook=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un facebook durumunu False yapayı unutmamak lazımmm dimi.
        post.facebook = False
        icerik = post.h1
        if not icerik:
            icerik = "Haberin devamı için tıklayın!"
        post.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinterest'])
        return HttpResponse(
            f"https://www.cocukmasallarioku.com/{'masal-oku' if post.Model == 'Masal' else 'hikaye-oku'}/{post.slug}/!={icerik} Daha fazla çocuk masal ve çocuk hikayeleri için sitemizi ziyaret edebilirsiniz !")
    else:
        return HttpResponse("post bulunamadı.")


@csrf_exempt
def linkedin_var_mi(request):
    post = SiirMasal.objects.filter(linkedin=True, aktif=True, status="Yayinda").order_by('-guncelleme_tarihi').first()
    if post is not None:
        # post'un facebook durumunu False yapayı unutmamak lazımmm dimi.
        post.linkedin = False
        icerik = post.h1
        if not icerik:
            icerik = "Haberin devamı için tıklayın!"
        post.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'linkedin', 'pinterest'])
        return HttpResponse(
            f"https://www.cocukmasallarioku.com/{'masal-oku' if post.Model == 'Masal' else 'hikaye-oku'}/{post.slug}/!={icerik} Daha fazla çocuk masal ve çocuk hikayeleri için sitemizi ziyaret edebilirsiniz !")
    else:
        return HttpResponse("post bulunamadı.")


@csrf_exempt
def twitter_var_mi(request):
    post = SiirMasal.objects.filter(twitter=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un indexing durumunu False yapayı unutmamak lazımmm dimi.
        post.twitter = False
        icerik = post.h1
        hashtag = "#masaloku #masal #hikaye"
        if not icerik:
            icerik = "Haberin devamı için tıklayın!"
        post.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinterest'])
        return HttpResponse(
            f"https://www.cocukmasallarioku.com/{'masal-oku' if post.Model == 'Masal' else 'hikaye-oku'}/{post.slug}/!={icerik} {hashtag} Daha Fazla Çocuk Masalı için Takipte Kalın!")
    else:
        return HttpResponse("Paylaşılacak Twitter içerik bulunamadı")


@csrf_exempt
def pintres_var_mi(request):
    post = SiirMasal.objects.filter(pinterest=True, aktif=True, status="Yayinda").order_by('-guncelleme_tarihi').first()
    if post is not None:
        # post'un facebook durumunu False yapayı unutmamak lazımmm dimi.
        post.pinterest = False
        icerik = post.h1
        if post.resim:
            image = post.resim.url
        else:
            image = "Yok"

        if post.Model == "Masal":
            KategoriFistName = post.masalKategorisi.first().MasalSlug
        if post.Model == "Hikaye":
            KategoriFistName = "Çocuk Hikayeleri"
        if not icerik:
            icerik = "Çocuk Masalları"
        post.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinterest'])
        return HttpResponse(
            f"https://www.cocukmasallarioku.com/{'masal-oku' if post.Model == 'Masal' else 'hikaye-oku'}/{post.slug}/!={icerik} Daha fazla çocuk masal ve çocuk hikayeleri için sitemizi ziyaret edebilirsiniz! !={post.title}!={KategoriFistName}!={image}")
    else:
        return HttpResponse("post bulunamadı.")


def mobilapp(request):
    title = "Çocuk masalları ve hikayeleri mobil uygulaması indir"
    description = "Çocuklara özel masallar, hikayeler ve oyunların olduğu süper mobil uygulama"
    keywords = "çocuk masalları, çocuk uygulaması, masal, hikaye, eğitici masal"

    context = {
        'title': title,
        'description': description,
        'keywords': keywords,

    }
    return render(request, 'system/Hepsi/mobilapp.html', context)


@csrf_exempt
def ai_add(request):
    if request.method == 'POST':
        # Gelen POST isteğindeki değerleri alın
        title = request.POST.get('title')
        h1 = request.POST.get('h1')
        icerik0 = request.POST.get('main')
        icerik1 = request.POST.get('icerik1')
        icerik2 = request.POST.get('icerik2')
        icerik3 = request.POST.get('icerik3')
        icerik4 = request.POST.get('icerik4')
        icerik5 = request.POST.get('icerik5')
        icerik6 = request.POST.get('icerik6')
        icerik7 = request.POST.get('icerik7')
        icerik8 = request.POST.get('icerik8')
        icerik9 = request.POST.get('icerik9')
        icerik10 = request.POST.get('icerik10')
        ZekaOzet = request.POST.get('ZekaOzet')
        faq = request.POST.get('faq')
        key = request.POST.get('key')
        meta = request.POST.get('meta')
        slug = request.POST.get('slug')

        Postislem = Blog(title=title, h1=h1, icerik=icerik0, icerik1=icerik1, icerik2=icerik2, icerik3=icerik3,
                         icerik4=icerik4, icerik5=icerik5,
                         icerik6=icerik6, icerik7=icerik7, icerik8=icerik8, icerik9=icerik9,
                         icerik10=icerik10, ozet=ZekaOzet, faq=faq, keywords=key,
                         meta_description=meta, slug=slug)
        Postislem.save()

        if Postislem.id is None:
            return HttpResponse("Post kaydedilemedi.")
        else:
            return HttpResponse("Şükürler Olsun Post başarıyla kaydedildi. ID: " + str(Postislem.id))


def flutter_masal_api(request):
    page_number = request.GET.get('page', 1)
    per_page = 10  # Her sayfada 10 masal

    masallar = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('-guncelleme_tarihi')
    paginator = Paginator(masallar, per_page)
    page_obj = paginator.get_page(page_number)

    data = []
    for masal in page_obj:
        data.append({
            'id': masal.id,
            'title': masal.title,
            'slug': masal.slug,
            'resim': masal.resim.url if masal.resim else None,
            'kisa_ozet': masal.meta_description[:100] + '...' if masal.meta_description else None,
        })

    return JsonResponse({
        'masallar': data,
        'has_next': page_obj.has_next(),
        'total_pages': paginator.num_pages,
    })


from .models import SiirMasal, Blog


def flutter_icerik_api(request):
    kategori = request.GET.get('kategori', 'masal')
    sayfa = int(request.GET.get('sayfa', 1))
    sayfa_basina = 10

    if kategori == 'masal':
        icerikler = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('-guncelleme_tarihi')
    elif kategori == 'hikaye':
        icerikler = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by(
            '-guncelleme_tarihi')
    elif kategori == 'cocuk':
        icerikler = Blog.objects.filter(aktif=True, status="Yayinda", Model="cocuk").order_by('-guncelleme_tarihi')
    else:
        return HttpResponse(json.dumps({"error": "Geçersiz kategori"}), content_type="application/json; charset=utf-8")

    baslangic = (sayfa - 1) * sayfa_basina
    bitis = baslangic + sayfa_basina
    sayfalanmis_icerikler = icerikler[baslangic:bitis]

    def clean_content(content):
        if content:
            content = strip_tags(content)
            content = html.unescape(content)
            content = force_str(content)
        return content

    data = [{
        'id': icerik.id,
        'slug': icerik.slug,
        'title': clean_content(icerik.title),
        'kisa_ozet': clean_content(icerik.meta_description)[:100] if icerik.meta_description else None,
        'resim': icerik.resim.url if icerik.resim else None,
    } for icerik in sayfalanmis_icerikler]

    return HttpResponse(json.dumps({
        'icerikler': data,
        'toplam_sayfa': (icerikler.count() + sayfa_basina - 1) // sayfa_basina,
        'mevcut_sayfa': sayfa,
    }, ensure_ascii=False), content_type="application/json; charset=utf-8")


def flutter_icerik_detay_api(request, slug):
    try:
        icerik = SiirMasal.objects.get(slug=slug, aktif=True, status="Yayinda")
        model_type = 'siirmasal'
    except SiirMasal.DoesNotExist:
        try:
            icerik = Blog.objects.get(slug=slug, aktif=True, status="Yayinda")
            model_type = 'blog'
        except Blog.DoesNotExist:
            return HttpResponse(json.dumps({"error": "İçerik bulunamadı"}),
                                content_type="application/json; charset=utf-8")

    def clean_content(content):
        if content:
            content = strip_tags(content)
            content = html.unescape(content)
            content = force_str(content)
        return content

    data = {
        'id': icerik.id,
        'title': clean_content(icerik.title),
        'model_type': model_type,
        'icerik': clean_content(icerik.icerik),
        'resim': icerik.resim.url if icerik.resim else None,
        'resim2': icerik.resim2.url if icerik.resim2 else None,
        'resim3': icerik.resim3.url if icerik.resim3 else None,
        'resim4': icerik.resim4.url if icerik.resim4 else None,
        'okunma_sayisi': icerik.okunma_sayisi,
        'yayin_tarihi': icerik.olusturma_tarihi.strftime("%d.%m.%Y"),
    }

    if model_type == 'blog':
        for i in range(1, 11):
            icerik_field = f'icerik{i}'
            if hasattr(icerik, icerik_field):
                data[icerik_field] = clean_content(getattr(icerik, icerik_field))
        data['ozet'] = clean_content(icerik.ozet)
        data['faq'] = clean_content(icerik.faq)
    else:
        data['icerik2'] = clean_content(icerik.icerik2)
        data['icerik3'] = clean_content(icerik.icerik3)
        data['icerik4'] = clean_content(icerik.icerik4)
        data['icerik5'] = clean_content(icerik.icerik5)
        data['icerik6'] = clean_content(icerik.icerik6)
        data['icerik7'] = clean_content(icerik.icerik7)
        data['icerik8'] = clean_content(icerik.icerik8)
        data['icerik9'] = clean_content(icerik.icerik9)
        data['icerik10'] = clean_content(icerik.icerik10)

    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json; charset=utf-8")


@vary_on_headers("Accept-Language")
@cache_page(60 * 60)
def matematik(request):
    game = get_object_or_404(Oyunlar, short_name="matematik")
    game.okunma_sayisi += 1
    game.save(update_fields=['okunma_sayisi'])
    BaskaMasal = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('?').first()
    BaskaHikaye = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by('?').first()

    context = {
        'game': game,
        'BaskaMasal': BaskaMasal,
        'BaskaHikaye': BaskaHikaye,
    }
    return render(request, 'system/Hepsi/matematik.html', context)


@vary_on_headers("Accept-Language")
@cache_page(60 * 60)
def hayvanoyunu(request):
    # Rastgele bir hayvan seçelim
    animal = Animals.objects.order_by('?').first()
    game = get_object_or_404(Oyunlar, short_name="hayvan")
    game.okunma_sayisi += 1
    game.save(update_fields=['okunma_sayisi'])

    BaskaMasal = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('?').first()
    BaskaHikaye = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by('?').first()

    # 3 adet rastgele hayvan ismi, biri doğru olacak
    other_animals = Animals.objects.exclude(id=animal.id).order_by('?')[:2]
    options = list(other_animals.values_list('ismi', flat=True)) + [animal.ismi]
    random.shuffle(options)

    # Mevcut resimleri bir liste içine alalım
    images = [animal.resim, animal.resim2, animal.resim3, animal.resim4, animal.resim5, animal.resim6]
    # Boş olmayan resimleri filtreleyelim
    valid_images = [img for img in images if img]
    # Eğer geçerli resim varsa, rastgele birini seçelim
    image = random.choice(valid_images) if valid_images else None

    # Mevcut sesleri bir liste içine alalım
    sounds = [animal.ses1, animal.ses2, animal.ses3]
    # Boş olmayan sesleri filtreleyelim
    valid_sounds = [sound for sound in sounds if sound]
    # Eğer geçerli ses varsa, rastgele birini seçelim
    sound = random.choice(valid_sounds) if valid_sounds else None

    context = {
        'animal': animal,
        'options': options,
        'game': game,
        'image': image,
        'sound': sound,
        'BaskaMasal': BaskaMasal,
        'BaskaHikaye': BaskaHikaye,
    }
    return render(request, 'system/Hepsi/yenihayvan.html', context)


def oyunlar(request):
    title = "Çocuklar İçin Eğitici Oyunlar - Çocuk Masalları"
    description = "Çocuklara özel oyunlar, matematik eişeştire oyunları, puzzle oyunları ve çok daha fazlası"
    keywords = "çocuk oyunları, eğitici oyunlar, oyun, matematik oyunları"

    context = {
        'title': title,
        'description': description,
        'keywords': keywords,

    }
    return render(request, 'system/Hepsi/oyunlar-listesi.html', context)


# Basit cache temizleme (her zaman 200 döner)
@csrf_exempt
def simple_clear_cache(request):
    try:
        cache.clear()
        return JsonResponse({"status": "success", "message": "cache cleared"}, status=200)
    except Exception:
        # Her durumda 200
        return JsonResponse({"status": "success", "message": "error but ok"}, status=200)


# Okunma sayısı artırma – SEO friendly (her zaman 200)
def increase_view_count(request):
    """
    SEO-friendly okuma sayısı artırma endpoint'i
    Her durumda 200 status döner (Google için)
    """
    try:
        if request.method == 'POST':
            # JSON parse etmeye çalış
            try:
                data = json.loads(request.body)
                object_id = data.get('object_id')
            except (json.JSONDecodeError, UnicodeDecodeError):
                # JSON parse hatası - sessizce başarılı dön
                return JsonResponse({'status': 'success', 'message': 'Ignored invalid data'}, status=200)

            if object_id:
                try:
                    obj = SiirMasal.objects.get(id=object_id)
                    obj.okunma_sayisi = F('okunma_sayisi') + 1  # Race condition'dan korunma
                    obj.save(update_fields=["okunma_sayisi"])
                    return JsonResponse({'status': 'success'}, status=200)
                except SiirMasal.DoesNotExist:
                    # Post bulunamadı ama sessizce başarılı dön
                    return JsonResponse({'status': 'success', 'message': 'Post not found but ok'}, status=200)
                except Exception:
                    # Veritabanı hatası ama yine 200 dön
                    return JsonResponse({'status': 'success', 'message': 'DB error but ok'}, status=200)
            else:
                # object_id yok ama 200 dön
                return JsonResponse({'status': 'success', 'message': 'No object_id but ok'}, status=200)
        else:
            # GET veya başka method - 200 dön
            return JsonResponse({'status': 'success', 'message': 'Method not POST but ok'}, status=200)

    except Exception:
        # Her türlü hata durumunda bile 200 dön (Google SEO için)
        return JsonResponse({'status': 'success', 'message': 'General error but ok'}, status=200)


def clean_content(content):
    if content:
        # HTML taglarını temizle
        content = strip_tags(content)
        # HTML entityleri düzelt (örn: &ccedil; -> ç)
        content = html.unescape(content)
        # String'e çevir
        content = force_str(content)
    return content


def get_story_detail(request, slug):
    try:
        story = SiirMasal.objects.get(slug=slug)
        story.okunma_sayisi += 1
        story.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinterest'])
        data = {
            'id': story.id,
            'title': clean_content(story.title),
            'icerik': clean_content(story.icerik),
            'icerik2': clean_content(story.icerik2),
            'icerik3': clean_content(story.icerik3),
            'icerik4': clean_content(story.icerik4),
            'icerik5': clean_content(story.icerik5),
            'icerik6': clean_content(story.icerik6),
            'icerik7': clean_content(story.icerik7),
            'icerik8': clean_content(story.icerik8),
            'icerik9': clean_content(story.icerik9),
            'icerik10': clean_content(story.icerik10),
            'resim': story.resim.url if story.resim else None,
            'resim2': story.resim2.url if story.resim2 else None,
            'resim3': story.resim3.url if story.resim3 else None,
            'resim4': story.resim4.url if story.resim4 else None,
            'resim5': story.resim5.url if story.resim5 else None,
            'resim6': story.resim6.url if story.resim6 else None,
            'resim7': story.resim7.url if story.resim7 else None,
            'resim8': story.resim8.url if story.resim8 else None,
            'resim9': story.resim9.url if story.resim9 else None,
            'resim10': story.resim10.url if story.resim10 else None,
        }
        return JsonResponse(data)
    except SiirMasal.DoesNotExist:
        return JsonResponse({'error': 'Story not found'}, status=404)

@csrf_exempt
def get_stories(request):
    page = int(request.GET.get('page', 1))
    stories = SiirMasal.objects.only(
        'id', 'title', 'slug', 'resim', 'meta_description', 'Model'
    ).filter(aktif=True, status="Yayinda").order_by('-guncelleme_tarihi')

    paginator = Paginator(stories, 25)
    current_page = paginator.page(page)

    data = {
        'results': [{
            'id': story.id,
            'title': clean_content(story.title),
            'slug': story.slug,
            'resim': story.resim.url if story.resim else None,
            'meta_description': clean_content(story.meta_description)[:100] if story.meta_description else "",
            'okunma': story.okunma_sayisi,
        } for story in current_page],
        'has_next': current_page.has_next(),
        'total_pages': paginator.num_pages
    }
    return JsonResponse(data)




@csrf_exempt
def get_categories(request):
    masal_categories = MasalKategorileri.objects.filter(Aktif=True)
    hikaye_categories = HikayeKategorileri.objects.filter(Aktif=True)

    categories = []

    # Masal kategorilerini ekle
    for category in masal_categories:
        categories.append({
            'id': category.id,
            'name': category.MasalKategoriAdi,
            'slug': category.MasalSlug,
            'h1': category.h1 if hasattr(category, 'h1') else None,
            'resim': category.resim.url if category.resim else "https://masalbucket.s3.amazonaws.com/static/images/masal/peri-masallari.webp",
            'type': 'Masal'
        })

    # Hikaye kategorilerini ekle
    for category in hikaye_categories:
        categories.append({
            'id': category.id,
            'name': category.HikayeKategoriAdi,
            'slug': category.HikayeSlug,
            'h1': category.h1 if hasattr(category, 'h1') else None,
            'resim': category.resim.url if category.resim else "https://masalbucket.s3.amazonaws.com/static/images/masal/peri-masallari.webp",
            'type': 'Hikaye'
        })

    return JsonResponse({'categories': categories})


@csrf_exempt
def get_category_stories(request, model_type, slug):
    try:
        page = int(request.GET.get('page', 1))

        # Model tipine göre kategoriyi bul
        if slug.lower() == 'masal':
            category = MasalKategorileri.objects.get(MasalSlug=model_type)
            stories = SiirMasal.objects.filter(
                masalKategorisi=category,
                Model='Masal',
                aktif=True
            )
        elif slug.lower() == 'hikaye':
            category = HikayeKategorileri.objects.get(HikayeSlug=model_type)
            stories = SiirMasal.objects.filter(
                hikayeKategorisi=category,
                Model='Hikaye',
                aktif=True
            )
        else:
            return JsonResponse({'error': f'Invalid model type={model_type}={slug}='}, status=400)

        stories = stories.only(
            'id', 'title', 'slug', 'resim',
            'meta_description', 'Model', 'okunma_sayisi'
        ).order_by('-guncelleme_tarihi')

        paginator = Paginator(stories, 25)
        current_page = paginator.page(page)

        data = {
            'results': [{
                'id': story.id,
                'title': clean_content(story.title),
                'slug': story.slug,
                'resim': story.resim.url if story.resim else None,
                'meta_description': clean_content(story.meta_description)[:100] if story.meta_description else "",
                'okunma': story.okunma_sayisi,
            } for story in current_page],
            'has_next': current_page.has_next(),
            'total_pages': paginator.num_pages
        }
        return JsonResponse(data)
    except (MasalKategorileri.DoesNotExist, HikayeKategorileri.DoesNotExist):
        return JsonResponse({'error': 'Category not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def ekle(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    # Gelen verileri al
    title = request.POST.get('title')
    h1 = request.POST.get('h1')
    slug = request.POST.get('slug')
    description = request.POST.get('description')
    keywords = request.POST.get('keywords')
    ozet = request.POST.get('ozet')
    faq = request.POST.get('faq')
    faq = json.loads(faq)
    resim = request.POST.get('resim')
    content1 = request.POST.get('content1')
    content2 = request.POST.get('content2')
    content3 = request.POST.get('content3')
    content4 = request.POST.get('content4')
    content5 = request.POST.get('content5')
    content6 = request.POST.get('content6')
    content7 = request.POST.get('content7')
    content8 = request.POST.get('content8')
    content9 = request.POST.get('content9')
    content10 = request.POST.get('content10')

    # short_title al ve kategori belirle
    short_title = request.POST.get('short_title')
    kategori = None
    if short_title == "bedtime":
        kategori = MasalKategorileri.objects.filter(MasalSlug="uyku-masallari").first()
    elif short_title == "peri":
        kategori = MasalKategorileri.objects.filter(MasalSlug="peri-masallari").first()
    elif short_title == "macera":
        kategori = MasalKategorileri.objects.filter(MasalSlug="macera-masallari").first()
    elif short_title == "hayvan":
        kategori = MasalKategorileri.objects.filter(MasalSlug="hayvan-masallari").first()
    elif short_title == "prenses":
        kategori = MasalKategorileri.objects.filter(MasalSlug="prenses-masallari").first()


    if resim:
        resim = f"3D cinematic film (caricature:0 2) [[{resim}]]"

    # Gerekli alanların doğrulanması
    if not title or not slug:
        return HttpResponseBadRequest("Title and slug are required")

    try:
        # Yeni bir Post oluştur
        post = SiirMasal.objects.create(
            title=title,
            h1=h1,
            slug=slugify(title),  # slug oluşturulurken sorun yaşanmasın diye
            meta_description=description,
            keywords=keywords,
            resimText=resim,
            icerik=content1,
            icerik2=content2,
            icerik3=content3,
            icerik4=content4,
            icerik5=content5,
            icerik6=content6,
            icerik7=content7,
            icerik8=content8,
            icerik9=content9,
            icerik10=content10,
            Model="Masal",
            faq=faq,
        )

        # Slug çakışmalarını engelle
        for _ in range(5):  # 5 deneme hakkı
            try:
                post.save()
                if kategori:
                    post.masalKategorisi.add(kategori)  # veya post.masalKategorisi.set([kategori])
                    post.save()
                break
            except IntegrityError:
                random_number = random.randint(3, 100)
                post.slug = f"{slugify(slug)}-{random_number}" if slug else f"{slugify(title)}-{random_number}"


        # Başarı yanıtı
        return JsonResponse({
            "status": "success",
            "message": "Post created successfully",
            "post_id": post.id,
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
def guncelle(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    # Slug bilgisini al
    slug = request.POST.get('slug')

    # Slug kontrolü
    if not slug:
        return HttpResponseBadRequest("Slug is required")

    try:
        # Slug'a göre Post'u bul
        post = SiirMasal.objects.get(slug=slug)

        # Gelen verileri al ve güncelle
        if 'title' in request.POST:
            post.title = request.POST.get('title')

        if 'h1' in request.POST:
            post.h1 = request.POST.get('h1')

        if 'description' in request.POST:
            post.meta_description = request.POST.get('description')

        if 'keywords' in request.POST:
            post.keywords = request.POST.get('keywords')

        if 'ozet' in request.POST:
            post.ozet = request.POST.get('ozet')

        if 'faq' in request.POST:
            try:
                post.faq = json.loads(request.POST.get('faq'))
            except:
                pass


        # İçerik alanlarını güncelle
        if 'content1' in request.POST:
            post.icerik = request.POST.get('content1')

        if 'content2' in request.POST:
            post.icerik2 = request.POST.get('content2')

        if 'content3' in request.POST:
            post.icerik3 = request.POST.get('content3')

        if 'content4' in request.POST:
            post.icerik4 = request.POST.get('content4')

        if 'content5' in request.POST:
            post.icerik5 = request.POST.get('content5')

        if 'content6' in request.POST:
            post.icerik6 = request.POST.get('content6')

        if 'content7' in request.POST:
            post.icerik7 = request.POST.get('content7')

        if 'content8' in request.POST:
            post.icerik8 = request.POST.get('content8')

        if 'content9' in request.POST:
            post.icerik9 = request.POST.get('content9')

        if 'content10' in request.POST:
            post.icerik10 = request.POST.get('content10')




        post.pinterest = True
        post.twitter = True
        post.facebook = True
        post.indexing = True
        post.linkedin = True

        # Değişiklikleri kaydet
        post.save()

        # Başarı yanıtı
        return JsonResponse({
            "status": "success",
            "message": "Post updated successfully",
            "post_id": post.id,
        })

    except SiirMasal.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Post not found with the given slug"}, status=404)

    except IntegrityError:
        # Slug çakışması durumunda
        return JsonResponse({"status": "error", "message": "Slug conflict occurred"}, status=400)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
def mobile_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user, created = MobileUser.objects.get_or_create(
                google_id=data['google_id'],
                defaults={
                    'username': data['name'],
                    'email': data['email'],
                    'photo': data['photo'],
                    'is_active': True,
                    'device_token': data.get('device_token'),
                    'last_login_platform': data.get('platform')
                }
            )

            # Kullanıcı zaten varsa bilgilerini güncelle
            if not created:
                user.username = data['name']
                user.device_token = data.get('device_token')
                user.last_login_platform = data.get('platform')
                user.update_last_login()
                user.save()

            response_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'photo': user.photo,
                'is_premium': user.is_premium,
                'is_ad_free': user.is_ad_free,
                'gold_balance': user.gold_balance,
                'premium_end_date': user.premium_end_date.isoformat() if user.premium_end_date else None,
                'ad_free_end_date': user.ad_free_end_date.isoformat() if user.ad_free_end_date else None
            }

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Diğer view'lar için kullanıcı kontrolü
def get_user_from_request(request):
    google_id = request.headers.get('X-GOOGLE-ID')
    try:
        return MobileUser.objects.get(google_id=google_id)
    except MobileUser.DoesNotExist:
        return None


@csrf_exempt
def add_favorite(request):
    if request.method == 'POST':
        user = get_user_from_request(request)
        if not user:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        try:
            data = json.loads(request.body)
            story_id = data.get('story_id')

            FavoriteStory.objects.create(
                user=user,
                story_id=story_id
            )

            return JsonResponse({'message': 'Success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)