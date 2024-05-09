from django.db import models
from Masallar.custom_storages import ImageSettingStorage

from django.conf import settings
from ckeditor.fields import RichTextField

HELP_TEXTS = {
    "title": "Masal Hiyenin başlığını girin.",
    "h1": "İçeriğin H1 Seo uyumlu girilmesi Lazım.",
    "Model": "Modele göre sılanma ve konumlandırılma olacaktır.",
    "yazar": "Şiiri yazan kullanıcıyı seçin.",
    "slug": "Şiirin URL'de görünecek kısmını girin.",
    "kategorisi": "Şiirin kategorisini seçin.",
    "sair": "Şiirin şairini seçin.",
    "icerik": "Şiirin içeriğini girin.",
    "kapak_resmi": "Anasayfa Resim",
    "status": "Şiirin durumunu seçin.",
    "aktif": "Şiirin aktif olup olmadığını belirtin.",
    "meta_title": "Sayfanın meta başlığını girin.",
    "meta_description": "Sayfanın meta açıklamasını girin.",
    "keywords": "Sayfanın anahtar kelimelerini \" Virgül '  ' \" ile ayrınız. ",
    "banner": "Ana Sayfadaki büyük resim alanında ögrünür",
    "small_banner": "Ana sayfada küçük resimlerde görünür.",
    "hakkinda": "Şiir hakkında anlatılmak istenen.",
    "Acikalama": "Kullanıcının işlem durumunu gösterir.",
}
status_cho = (
    ("Taslak", "Taslak"),
    ("Hazir", "Hazir"),
    ("Yayinda", "Yayinda"),
    ("oto", "oto"),
    ("manuel", "manuel"),
)

model_tipi = (
    ("Hikaye", "Hikaye"),
    ("Masal", "Masal"),
)

boyutu = (
    ("Kısa", "Kısa"),
    ("Uzun", "Uzun"),
)

def kapak_resmi_upload_to(instance, filename):
    # Dosya adını değiştir
    yeni_ad = f"{instance.slug}"
    # Dosya uzantısını koru
    uzanti = filename.split('.')[-1]
    # Yeni dosya adını döndür
    return f"kapak_resimleri/{yeni_ad}.{uzanti}"

class HikayeKategorileri(models.Model):
    HikayeKategoriAdi = models.CharField(max_length=255, blank=True)
    HikayeSlug = models.SlugField(max_length=255, blank=True)
    Hikaye_Title = models.TextField( blank=True, null=True)
    Hikaye_meta_description = models.TextField( blank=True, null=True, help_text=HELP_TEXTS["meta_description"])
    Hikaye_keywords = models.CharField(max_length=255,blank=True,null=True,help_text=HELP_TEXTS["keywords"])
    sirasi = models.IntegerField(default=100)
    Aktif = models.BooleanField(default=False)
    Banner = models.BooleanField(default=False)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hikayeler Kategorileri"
    def __str__(self):
        return self.HikayeKategoriAdi


class MasalKategorileri(models.Model):
    MasalKategoriAdi = models.CharField(max_length=255, unique=True)
    MasalSlug = models.SlugField(max_length=255, unique=True, blank=True)
    Masal_Title = models.TextField(blank=True, null=True)
    Masal_meta_description = models.TextField( blank=True, help_text=HELP_TEXTS["meta_description"])
    Masal_keywords = models.CharField( max_length=255, blank=True,  help_text=HELP_TEXTS["keywords"])
    sirasi = models.IntegerField(default=100)
    Aktif = models.BooleanField(default=False)
    Banner = models.BooleanField(default=False)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Masallar Kategorileri"
    def __str__(self):
        return self.MasalKategoriAdi



# Create your models here.
class SiirMasal(models.Model):
    title = models.CharField(max_length=255, help_text=HELP_TEXTS["title"])
    slug = models.SlugField(max_length=255, unique=True, blank=True,help_text=HELP_TEXTS["slug"])
    h1 = models.CharField(max_length=255,blank=True, help_text=HELP_TEXTS["h1"])
    Model = models.CharField(max_length=40, choices=model_tipi, help_text=HELP_TEXTS["Model"])
    masalKategorisi = models.ManyToManyField(MasalKategorileri, blank=True, help_text="Şiirin alt kategorilerini seçin.")
    hikayeKategorisi = models.ManyToManyField(HikayeKategorileri, blank=True, help_text="Şiirin alt kategorilerini seçin.")
    icerik = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    icerik2 = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    icerik3 = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    icerik4 = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    uzunluk = models.CharField(max_length=25, choices=boyutu, default="Kısa", help_text=HELP_TEXTS["status"])
    youtube = models.URLField(blank=True)
    meta_description = models.TextField(blank=True,verbose_name="Meta Açıklama",help_text=HELP_TEXTS["meta_description"])
    keywords = models.CharField(max_length=255,blank=True,verbose_name="Anahtar Kelimeler",help_text=HELP_TEXTS["keywords"])
    yayin_tarihi = models.DateTimeField(null=True, blank=True, help_text="Postanın yayınlanacağı tarih ve saat")
    status = models.CharField(max_length=10, choices=status_cho, default="Taslak", help_text=HELP_TEXTS["status"])
    aktif = models.BooleanField(default=False, help_text=HELP_TEXTS["aktif"])
    banner = models.BooleanField(default=False, help_text=HELP_TEXTS["banner"])
    small_banner = models.BooleanField(default=False,help_text=HELP_TEXTS["small_banner"])
    indexing = models.BooleanField(default=False, help_text="Indexlensin mi?")
    facebook = models.BooleanField(default=True, help_text="Facebook da Paylaşılsın mı ?")
    twitter = models.BooleanField(default=True, help_text="twitter da Paylaşılsın mı ?")
    okunma_sayisi = models.PositiveBigIntegerField(default=0)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    def kelime_sayisi(self):
        return len(self.icerik.split())
    class Meta:
        verbose_name_plural = "Post"
    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=255, help_text=HELP_TEXTS["title"])
    slug = models.SlugField(max_length=255, unique=True, blank=True,help_text=HELP_TEXTS["slug"])
    h1 = models.CharField(max_length=255,blank=True, help_text=HELP_TEXTS["h1"])
    icerik = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    icerik1 = RichTextField(null=True, blank=True)
    icerik2 = RichTextField(null=True, blank=True)
    icerik3 = RichTextField(null=True, blank=True)
    icerik4 = RichTextField(null=True, blank=True)
    icerik5 = RichTextField(null=True, blank=True)
    icerik6 = RichTextField(null=True, blank=True)
    icerik7 = RichTextField(null=True, blank=True)
    icerik8 = RichTextField(null=True, blank=True)
    icerik9 = RichTextField(null=True, blank=True)
    icerik10 = RichTextField(null=True, blank=True)
    ozet = models.TextField(blank=True, verbose_name="Özet")
    faq = models.TextField(blank=True, verbose_name="Faq")
    resim = models.ImageField(upload_to=kapak_resmi_upload_to,
                              storage=ImageSettingStorage(),
                              null=True, blank=True)
    resim2 = models.ImageField(upload_to=kapak_resmi_upload_to,
                              storage=ImageSettingStorage(),
                              null=True, blank=True)
    resim3 = models.ImageField(upload_to=kapak_resmi_upload_to,
                              storage=ImageSettingStorage(),
                              null=True, blank=True)
    resim4 = models.ImageField(upload_to=kapak_resmi_upload_to,
                              storage=ImageSettingStorage(),
                              null=True, blank=True)

    youtube = models.URLField(blank=True)
    meta_description = models.TextField(blank=True,verbose_name="Meta Açıklama",help_text=HELP_TEXTS["meta_description"])
    keywords = models.CharField(max_length=255,blank=True,verbose_name="Anahtar Kelimeler",help_text=HELP_TEXTS["keywords"])
    yayin_tarihi = models.DateTimeField(null=True, blank=True, help_text="Postanın yayınlanacağı tarih ve saat")
    status = models.CharField(max_length=10, choices=status_cho, default="Taslak", help_text=HELP_TEXTS["status"])
    aktif = models.BooleanField(default=False, help_text=HELP_TEXTS["aktif"])
    banner = models.BooleanField(default=False, help_text=HELP_TEXTS["banner"])
    small_banner = models.BooleanField(default=False,help_text=HELP_TEXTS["small_banner"])
    okunma_sayisi = models.PositiveBigIntegerField(default=0)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Blog"
    def __str__(self):
        return self.title



class iletisimmodel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255,blank=True,null=True,help_text=HELP_TEXTS["keywords"])
    title = models.TextField( blank=True, null=True)
    icerik = models.TextField( blank=True, null=True, help_text=HELP_TEXTS["meta_description"])
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "iletişim Formu"
    def __str__(self):
        return self.title