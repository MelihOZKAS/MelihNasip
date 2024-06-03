from django.shortcuts import render, HttpResponse, get_object_or_404, reverse
from .models import SiirMasal, HikayeKategorileri, MasalKategorileri, iletisimmodel, Blog
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import re
from django.utils.html import strip_tags
from html import unescape


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
    alt_kategori = get_object_or_404(MasalKategorileri, MasalSlug=alt_kategori_slug)
    icerik_list = SiirMasal.objects.filter(masalKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                           Model="Masal").order_by('-olusturma_tarihi')
    sayfa_adi = f"En Güzel {alt_kategori.MasalKategoriAdi}"
    sayfa_Turu = "Masal"

    paginator = Paginator(icerik_list, 10)  # 10 içerik göstermek için
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


def MasalOkuListesi(request):
    icerik_list = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('-olusturma_tarihi')[
                  :50]
    sayfa_adi = f"Çocuklara Uyku Öncesi Masal Oku"
    sayfa_Turu = "Masal"

    paginator = Paginator(icerik_list, 14)  # 10 içerik göstermek için
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    title = "Çocuk Masalları | Uyku Masalları | Kısa Masal | Masal Oku"
    description = "Çocuklarınızın hayal dünyasını genişletmek ve onlara keyifli anlar yaşatmak için Masal Oku sayfamızı ziyaret edin. Uyku öncesi masallar ve kısa masal oku"
    Keys = "Masal Oku, Çocuk Masalları, Eğitici Masallar, Eğlenceli Masallar, Öğretici Masallar, Fantastik Masallar, İlgi Çekici Masallar, En İyi Masallar, En Güzel Masallar, Popüler Masallar"

    if page_number is None:
        title = title
        description = description
    else:
        title = f"{title} - {page_number}"
        description = f"{description} - Sayfa {page_number}"

    context = {
        'title': title,
        'description': description,
        'keywords': Keys,
        'alt_kategori': "YOKKKKKK",
        'icerik': icerik,
        'sayfa_adi': sayfa_adi,
        'sayfa_Turu': sayfa_Turu,
    }
    return render(request, 'system/Hepsi/oku-url-detay-yeni.html', context)


def hikayeAltKategori(request, alt_kategori_slug):
    alt_kategori = get_object_or_404(HikayeKategorileri, HikayeSlug=alt_kategori_slug)
    icerik_list = SiirMasal.objects.filter(hikayeKategorisi=alt_kategori, aktif=True, status="Yayinda",
                                           Model="Hikaye").order_by('-olusturma_tarihi')
    sayfa_adi = f"En Güzel {alt_kategori.HikayeKategoriAdi}"
    sayfa_Turu = "Hikaye"

    paginator = Paginator(icerik_list, 10)  # 10 içerik göstermek için
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


def hikayeOkuListesi(request):
    icerik_list = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by('-olusturma_tarihi')[
                  :50]
    sayfa_adi = f"En Güzel Çocuk Hikayeleri Oku"
    sayfa_Turu = "Hikaye"

    paginator = Paginator(icerik_list, 10)  # 10 içerik göstermek için
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    title = "Aile Hikayeleri, Dini Hikaye En Güzel Hikayeler | Hikaye Oku"
    description = "Çocuklarınızın hayal dünyasını genişletmek ve onlara keyifli anlar yaşatmak için Hikaye Oku sayfamızı ziyaret edin. Çocuklara özel  uzun hikaye oku ve dinle"
    Keys = "Hikaye Oku, Çocuk Hikayeleri, Eğitici Hikayeleri, Eğlenceli Hikayeleri, Öğretici Hikayeleri, Fantastik Hikayeleri, ingilizce Hikayeler, En İyi hikayeler, En Güzel Hikayeler, Popüler Hikayeler"

    if page_number is None:
        title = title
        description = description
    else:
        title = f"{title} - {page_number}"
        description = f"{description} - Sayfa {page_number}"

    context = {
        'title': title,
        'description': description,
        'keywords': Keys,
        'alt_kategori': "YOKKKKKK",
        'icerik': icerik,
        'sayfa_adi': sayfa_adi,
        'sayfa_Turu': sayfa_Turu,
    }
    return render(request, 'system/Hepsi/oku-url-detay-yeni.html', context)


def BlogHome(request):
    if request.resolver_match.url_name == 'cocuk':
        icerik_list = Blog.objects.filter(aktif=True, status="Yayinda", Model="cocuk").order_by('-olusturma_tarihi')
        keywords = "Çocuk Gelişimi, Fiziksel Gelişim, Duygusal Gelişim, Zihinsel Gelişim, Çocuk Psikolojisi, Ebeveynlik İpuçları, çocuk gelişimi kitapları, çocuk gelişimi masalları, çocuk gelişimi hikayeleri",
        sayfa_adi = f"Çocuk Gelişimi Bilimsel Araştırmalarla Desteklenen Pratik Bilgiler"
        title = f"Çocuk Gelişimi Araştırmalar ve Pratik Bilgi | Masal Oku"
        description = f"Çocuk gelişimindeki en son bilimsel bulguları ve pratik bilgiler. Çocuğunuzun fiziksel, duygusal ve zihinsel gelişimini destekler."

    elif request.resolver_match.url_name == 'saglik':
        icerik_list = Blog.objects.filter(aktif=True, status="Yayinda", Model="saglik").order_by('-olusturma_tarihi')
        keywords = "Çocuk Gelişimi, Fiziksel Gelişim, Duygusal Gelişim, Zihinsel Gelişim, Çocuk Psikolojisi, Ebeveynlik İpuçları, çocuk gelişimi kitapları, çocuk gelişimi masalları, çocuk gelişimi hikayeleri",
        sayfa_adi = f"Çocuk Gelişimi Bilimsel Araştırmalarla Desteklenen Pratik Bilgiler"
        title = f"Çocuk Gelişimi Araştırmalar ve Pratik Bilgi | Masal Oku"
        description = f"Çocuk gelişimindeki en son bilimsel bulguları ve pratik bilgiler. Çocuğunuzun fiziksel, duygusal ve zihinsel gelişimini destekler."

    elif request.resolver_match.url_name == 'kadin':
        icerik_list = Blog.objects.filter(aktif=True, status="Yayinda", Model="kadin").order_by('-olusturma_tarihi')
        keywords = "Çocuk Gelişimi, Fiziksel Gelişim, Duygusal Gelişim, Zihinsel Gelişim, Çocuk Psikolojisi, Ebeveynlik İpuçları, çocuk gelişimi kitapları, çocuk gelişimi masalları, çocuk gelişimi hikayeleri",
        sayfa_adi = f"Çocuk Gelişimi Bilimsel Araştırmalarla Desteklenen Pratik Bilgiler"
        title = f"Çocuk Gelişimi Araştırmalar ve Pratik Bilgi | Masal Oku"
        description = f"Çocuk gelişimindeki en son bilimsel bulguları ve pratik bilgiler. Çocuğunuzun fiziksel, duygusal ve zihinsel gelişimini destekler."



    paginator = Paginator(icerik_list, 10)  # 10 içerik göstermek için
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    if page_number is None:
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
    return render(request, 'system/Hepsi/bloghome.html', context)


def Masallar(request):
    Tum_Masallar = MasalKategorileri.objects.filter(Aktif=True).order_by('sirasi')

    title = "Çocuk Masallı, Çocuklara Uyku Masalları | Masal Oku"
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

        return HttpResponse(
            'İletişim istediğinizi Kaydettik. <a href="{}" class="btn btn-primary">Ana Sayfaya Dönmek için Tıklayın.</a>'.format(
                reverse('home')))

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


def cerez(request):
    context = {
        'title': "Çocuk Hikayeleri ve Masalları Oku - Çerez Politikası",
        'description': "Çocuk hiyakeleri ve Masalları sitemizin Çerez Politikası bölümüdür. Masal ve Hikayeler için iletişime geçebilirsiniz.",
        'keywords': "Çocuk masalları, uyku masalları, uzun uyku hikayeleri, en güzel çocuk hikayeleri, uyku getiren masallar, keloğlan masalları, 6 yaş çocuk masalları",
    }

    return render(request, 'system/Hepsi/cerez.html', context)


def kullanim(request):
    context = {
        'title': "Çocuk Masallarını Dinle - Kullanım Şartları | Masal Oku",
        'description': "Çocuk hiyakeleri ve Masalları sitemizin Kullanım Şartları bölümüdür. Masal ve Hikayeler için iletişime geçebilirsiniz.",
        'keywords': "Çocuk masalları, eğitici masallar, uyku masalları, uzun uyku hikayeleri, keloğlan masalları, en güzel çocuk hikayeleri, uyku getiren masallar, keloğlan masalları",

    }

    return render(request, 'system/Hepsi/kullanim.html', context)


def enderunMasal(request, masal_slug):
    EnDerun = get_object_or_404(SiirMasal, slug=masal_slug, aktif=True, status="Yayinda")
    EnDerun.okunma_sayisi += 1  # okunma sayısını artır
    EnDerun.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinterest'])
    BaskaMasal = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('?').first()
    BaskaHikaye = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by('?').first()
    thumbnail_url = None

    if EnDerun.Model == 'Masal':
        categories = EnDerun.masalKategorisi.all()
    elif EnDerun.Model == 'Hikaye':
        categories = EnDerun.hikayeKategorisi.all()

    category_names = [category.MasalKategoriAdi for category in categories]
    category_names_str = ', '.join(category_names)

    if EnDerun.youtube:
        youtube_id = get_youtube_id(EnDerun.youtube)
        thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/0.jpg"

    if not category_names:
        category_names_str = EnDerun.Model



    contents = [EnDerun.icerik, EnDerun.icerik2, EnDerun.icerik3, EnDerun.icerik4]
    articleBody = ' '.join(filter(None, contents))


    resimler = []
    if EnDerun.resim:
        resimler.append(EnDerun.resim.url)
    if EnDerun.resim2:
        resimler.append(EnDerun.resim2.url)
    if EnDerun.resim3:
        resimler.append(EnDerun.resim3.url)
    if EnDerun.resim4:
        resimler.append(EnDerun.resim4.url)
    if not resimler:  # Eğer resimler listesi boşsa
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
    return render(request, 'system/Hepsi/enderun.html', context)


def enderunBlog(request, blog_slug):
    EnDerun = get_object_or_404(Blog, slug=blog_slug, aktif=True, status="Yayinda")
    EnDerun.okunma_sayisi += 1  # okunma sayısını artır
    EnDerun.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinterest'])
    BaskaMasal = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('?').first()
    BaskaHikaye = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by('?').first()
    category_names_str = "Çocuk Gelişimi"
    thumbnail_url = None

    if EnDerun.youtube:
        youtube_id = get_youtube_id(EnDerun.youtube)
        thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/0.jpg"

    contents = [EnDerun.icerik, EnDerun.icerik1, EnDerun.icerik2, EnDerun.icerik3, EnDerun.icerik4, EnDerun.icerik5,
                EnDerun.icerik6, EnDerun.icerik7, EnDerun.icerik8, EnDerun.icerik9, EnDerun.icerik10]
    articleBody = ' '.join(filter(None, contents))


    resimler = []

    if EnDerun.resim:
        resimler.append(EnDerun.resim.url)
    if EnDerun.resim2:
        resimler.append(EnDerun.resim2.url)
    if EnDerun.resim3:
        resimler.append(EnDerun.resim3.url)
    if EnDerun.resim4:
        resimler.append(EnDerun.resim4.url)

    if not resimler:  # Eğer resimler listesi boşsa
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
    return render(request, 'system/Hepsi/blog-Enderun.html', context)


def enderunHikaye(request, hikaye_slug):
    EnDerun = get_object_or_404(SiirMasal, slug=hikaye_slug, aktif=True, status="Yayinda")
    EnDerun.okunma_sayisi += 1  # okunma sayısını artır
    EnDerun.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinterest'])
    BaskaMasal = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Masal").order_by('?').first()
    BaskaHikaye = SiirMasal.objects.filter(aktif=True, status="Yayinda", Model="Hikaye").order_by('?').first()
    thumbnail_url = None

    if EnDerun.Model == 'Masal':
        categories = EnDerun.masalKategorisi.all()
    elif EnDerun.Model == 'Hikaye':
        categories = EnDerun.hikayeKategorisi.all()

    category_names = [category.HikayeKategoriAdi for category in categories]
    category_names_str = ', '.join(category_names)
    if EnDerun.youtube:
        youtube_id = get_youtube_id(EnDerun.youtube)
        thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/0.jpg"

    if not category_names:
        category_names_str = EnDerun.Model


    contents = [EnDerun.icerik, EnDerun.icerik2, EnDerun.icerik3, EnDerun.icerik4]
    articleBody = ' '.join(filter(None, contents))


    resimler = []
    if EnDerun.resim:
        resimler.append(EnDerun.resim.url)
    if EnDerun.resim2:
        resimler.append(EnDerun.resim2.url)
    if EnDerun.resim3:
        resimler.append(EnDerun.resim3.url)
    if EnDerun.resim4:
        resimler.append(EnDerun.resim4.url)

    if not resimler:  # Eğer resimler listesi boşsa
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
    return render(request, 'system/Hepsi/enderun.html', context)


@require_GET
def robots_txt(request):
    return HttpResponse(robots_txt_content, content_type="text/plain")


robots_txt_content = """
User-agent: *
Allow: /
Sitemap: https://www.cocukmasallarioku.com/sitemap.xml
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
            #post.indexing = True  # indekslendi olarak işaretle
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
def pintres_var_mi(request):
    post = SiirMasal.objects.filter(pinterest=True, aktif=True, Model="Masal", status="Yayinda").first()
    if post is not None:
        # post'un facebook durumunu False yapayı unutmamak lazımmm dimi.
        post.pinterest = False
        icerik = post.h1
        if post.resim:
            image = post.resim.url
        else:
            image = "Yok"

        if post.Model =="Masal":
            KategoriFistName = post.masalKategorisi.first().MasalSlug
        if post.Model =="Hikaye":
            KategoriFistName = post.hikayeKategorisi.first().HikayeSlug
        if not icerik:
            icerik = "Haberin devamı için tıklayın!"
        post.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinterest'])
        return HttpResponse(
            f"https://www.cocukmasallarioku.com/{'masal-oku' if post.Model == 'Masal' else 'hikaye-oku'}/{post.slug}/!={icerik} Daha fazla çocuk masal ve çocuk hikayeleri için sitemizi ziyaret edebilirsiniz! !={post.title}!={KategoriFistName}!={image}")
    else:
        return HttpResponse("post bulunamadı.")
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
