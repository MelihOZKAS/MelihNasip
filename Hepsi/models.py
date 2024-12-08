from django.db import models
from Masallar.custom_storages import *
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from ckeditor.fields import RichTextField
from django.apps import apps

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

model_tipi_blog = (
    ("saglik", "saglik"),
    ("kadin", "kadin"),
    ("cocuk", "cocuk"),
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
def kategori_kapak_resmi_upload_to(instance, filename):
    # Dosya adını değiştir
    yeni_ad = f"{instance.MasalSlug}"
    # Dosya uzantısını koru
    uzanti = filename.split('.')[-1]
    # Yeni dosya adını döndür
    return f"masal-kategori-kapak_resimleri/{yeni_ad}.{uzanti}"

class HikayeKategorileri(models.Model):
    HikayeKategoriAdi = models.CharField(max_length=255, blank=True)
    HikayeSlug = models.SlugField(max_length=255, blank=True)
    Hikaye_Title = models.TextField( blank=True, null=True)
    h1 = models.CharField(max_length=255, blank=True, null=True)
    kisa_title = models.TextField(blank=True, null=True)
    kisa_aciklama = models.TextField(blank=True, null=True)
    Hikaye_meta_description = models.TextField( blank=True, null=True, help_text=HELP_TEXTS["meta_description"])
    Hikaye_keywords = models.CharField(max_length=255,blank=True,null=True,help_text=HELP_TEXTS["keywords"])
    sirasi = models.IntegerField(default=100)
    Aktif = models.BooleanField(default=False)
    Banner = models.BooleanField(default=False)
    resim = models.ImageField(upload_to=kapak_resmi_upload_to,
                              storage=ImageSettingStorage(),
                              null=True, blank=True)
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
    h1 = models.CharField(max_length=255, blank=True, null=True)
    kisa_title = models.TextField(blank=True, null=True)
    kisa_aciklama = models.TextField(blank=True, null=True)
    Masal_meta_description = models.TextField( blank=True, help_text=HELP_TEXTS["meta_description"])
    Masal_keywords = models.CharField(max_length=255, blank=True,  help_text=HELP_TEXTS["keywords"])
    sirasi = models.IntegerField(default=100)
    Aktif = models.BooleanField(default=False)
    Banner = models.BooleanField(default=False)
    resim = models.ImageField(upload_to=kategori_kapak_resmi_upload_to,
                              storage=ImageSettingStorage(),
                              null=True, blank=True)
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
    icerik5 = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    icerik6 = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    icerik7 = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    icerik8 = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    icerik9 = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    icerik10 = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
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
    resim5 = models.ImageField(upload_to=kapak_resmi_upload_to,
                               storage=ImageSettingStorage(),
                               null=True, blank=True)
    resim6 = models.ImageField(upload_to=kapak_resmi_upload_to,
                               storage=ImageSettingStorage(),
                               null=True, blank=True)
    resim7 = models.ImageField(upload_to=kapak_resmi_upload_to,
                               storage=ImageSettingStorage(),
                               null=True, blank=True)
    resim8 = models.ImageField(upload_to=kapak_resmi_upload_to,
                               storage=ImageSettingStorage(),
                               null=True, blank=True)
    resim9 = models.ImageField(upload_to=kapak_resmi_upload_to,
                               storage=ImageSettingStorage(),
                               null=True, blank=True)
    resim10 = models.ImageField(upload_to=kapak_resmi_upload_to,
                               storage=ImageSettingStorage(),
                               null=True, blank=True)
    uzunluk = models.CharField(max_length=25, choices=boyutu, default="Kısa", help_text=HELP_TEXTS["status"])
    youtube = models.URLField(blank=True)
    meta_description = models.TextField(blank=True,verbose_name="Meta Açıklama",help_text=HELP_TEXTS["meta_description"])
    keywords = models.CharField(max_length=255,blank=True,verbose_name="Anahtar Kelimeler",help_text=HELP_TEXTS["keywords"])
    resimText = models.TextField(blank=True,)
    yayin_tarihi = models.DateTimeField(null=True, blank=True, help_text="Postanın yayınlanacağı tarih ve saat")
    status = models.CharField(max_length=10, choices=status_cho, default="Taslak", help_text=HELP_TEXTS["status"])
    aktif = models.BooleanField(default=False, help_text=HELP_TEXTS["aktif"])
    banner = models.BooleanField(default=False, help_text=HELP_TEXTS["banner"])
    small_banner = models.BooleanField(default=False,help_text=HELP_TEXTS["small_banner"])
    indexing = models.BooleanField(default=False, help_text="Indexlensin mi?")
    facebook = models.BooleanField(default=True, help_text="Facebook da Paylaşılsın mı ?")
    linkedin = models.BooleanField(default=True, help_text="Linkedin de Paylaşılsın mı ?")
    twitter = models.BooleanField(default=True, help_text="twitter da Paylaşılsın mı ?")
    pinterest = models.BooleanField(default=True, help_text="twitter da Paylaşılsın mı ?")
    okunma_sayisi = models.PositiveBigIntegerField(default=0)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    def kelime_sayisi(self):
        toplam_kelime_sayisi = 0
        icerikler = [self.icerik, self.icerik2, self.icerik3, self.icerik4, self.icerik5, self.icerik6, self.icerik7, self.icerik8, self.icerik9, self.icerik10]
        for icerik in icerikler:
            if icerik:
                toplam_kelime_sayisi += len(icerik.split())
        return toplam_kelime_sayisi
    class Meta:
        verbose_name_plural = "Post"
    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=255, help_text=HELP_TEXTS["title"])
    slug = models.SlugField(max_length=255, unique=True, blank=True,help_text=HELP_TEXTS["slug"])
    h1 = models.CharField(max_length=255,blank=True, help_text=HELP_TEXTS["h1"])
    Model = models.CharField(max_length=40, choices=model_tipi_blog, help_text=HELP_TEXTS["Model"],  blank=True)
    icerik = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    icerik1 = RichTextField(null=True, blank=True)
    #froaicerik1 = FroalaField(null=True, blank=True)
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
    indexing = models.BooleanField(default=True, help_text="Indexlensin mi?")
    facebook = models.BooleanField(default=True, help_text="Facebook da Paylaşılsın mı ?")
    twitter = models.BooleanField(default=True, help_text="twitter da Paylaşılsın mı ?")
    pinterest = models.BooleanField(default=True, help_text="twitter da Paylaşılsın mı ?")
    linkedin = models.BooleanField(default=True, help_text="Linkedin de Paylaşılsın mı ?")
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
    title = models.TextField(blank=True, null=True)
    icerik = models.TextField(blank=True, null=True, help_text=HELP_TEXTS["meta_description"])
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "iletişim Formu"
    def __str__(self):
        return self.title




class Oyunlar(models.Model):
    title = models.CharField(max_length=255, blank=True)
    h1 = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, verbose_name="Meta Açıklama")
    keywords = models.CharField(max_length=255, blank=True, verbose_name="Anahtar Kelimeler")
    okunma_sayisi = models.PositiveBigIntegerField(default=0)
    oyun_turu = models.CharField(max_length=100, verbose_name="Oyun Türü", blank=True, null=True)
    short_name = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.title



class Animals(models.Model):
    ismi = models.CharField(max_length=50, blank=True)
    ingilizce_ismi = models.CharField(max_length=50, blank=True)
    game_meta = models.ForeignKey(Oyunlar, on_delete=models.CASCADE, related_name="animal_game", blank=True, null=True)


    ses1 = models.FileField(upload_to='sounds/', blank=True, storage=MediaStorage())
    ses2 = models.FileField(upload_to='sounds/', blank=True, storage=MediaStorage())
    ses3 = models.FileField(upload_to='sounds/', blank=True, storage=MediaStorage())
    ingilizce_ses = models.FileField(upload_to='sounds/', blank=True, storage=MediaStorage())


    resim = models.ImageField(upload_to='Hayvan-images/',
                              storage=ImageSettingStorage(),
                              null=True, blank=True)
    resim2 = models.ImageField(upload_to='Hayvan-images/',
                              storage=ImageSettingStorage(),
                              null=True, blank=True)
    resim3 = models.ImageField(upload_to='Hayvan-images/',
                              storage=ImageSettingStorage(),
                              null=True, blank=True)
    resim4 = models.ImageField(upload_to='Hayvan-images/',
                              storage=ImageSettingStorage(),
                              null=True, blank=True)
    resim5 = models.ImageField(upload_to='Hayvan-images/',
                              storage=ImageSettingStorage(),
                              null=True, blank=True)
    resim6 = models.ImageField(upload_to='Hayvan-images/',
                              storage=ImageSettingStorage(),
                              null=True, blank=True)


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class customuser(AbstractUser):
    """Özelleştirilmiş kullanıcı modeli"""
    # Sosyal login bilgileri
    google_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    apple_id = models.CharField(max_length=100, blank=True, null=True, unique=True)

    # Abonelik durumları
    is_premium = models.BooleanField(default=False)
    premium_end_date = models.DateTimeField(null=True, blank=True)
    is_ad_free = models.BooleanField(default=False)
    ad_free_end_date = models.DateTimeField(null=True, blank=True)

    # Gold (Altın) sistemi
    gold_balance = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    total_earned_gold = models.PositiveIntegerField(default=0)
    last_reward_ad_time = models.DateTimeField(null=True, blank=True)

    # Kullanıcının masal etkileşimleri
    favorite_stories = models.ManyToManyField(
        'SiirMasal',
        through='FavoriteStory',
        related_name='favorited_by',
        blank=True
    )
    will_read_stories = models.ManyToManyField(
        'SiirMasal',
        through='WillReadStory',
        related_name='will_be_read_by',
        blank=True
    )
    read_stories = models.ManyToManyField(
        'SiirMasal',
        through='ReadingHistory',
        related_name='read_by',
        blank=True
    )

    # Platform bilgileri
    device_token = models.CharField(max_length=255, blank=True, null=True)
    last_login_platform = models.CharField(
        max_length=10,
        choices=[('IOS', 'iOS'), ('ANDROID', 'Android')],
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'users'  # Tablo adını değiştirdim
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
        swappable = 'AUTH_USER_MODEL'
        app_label = 'Hepsi'  # Bu satırı ekledim


class FavoriteStory(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    story = models.ForeignKey('SiirMasal', on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'favorite_stories'
        unique_together = ['user', 'story']
        ordering = ['-added_date']


class WillReadStory(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    story = models.ForeignKey('SiirMasal', on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    planned_date = models.DateTimeField(null=True, blank=True)
    reminder = models.BooleanField(default=False)

    class Meta:
        db_table = 'will_read_stories'
        unique_together = ['user', 'story']
        ordering = ['-added_date']


class ReadingHistory(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    story = models.ForeignKey('SiirMasal', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    last_read_date = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    last_position = models.IntegerField(default=0)
    reading_duration = models.PositiveIntegerField(default=0)
    child_reaction = models.CharField(
        max_length=20,
        choices=[
            ('LOVED', 'Çok Sevdi'),
            ('LIKED', 'Beğendi'),
            ('NEUTRAL', 'Nötr'),
            ('DISLIKED', 'Beğenmedi')
        ],
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'reading_history'
        unique_together = ['user', 'story']
        ordering = ['-last_read_date']


class PurchaseHistory(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    product_id = models.CharField(max_length=100)
    purchase_token = models.CharField(max_length=255)
    platform = models.CharField(
        max_length=10,
        choices=[('IOS', 'iOS'), ('ANDROID', 'Android')]
    )
    subscription_type = models.CharField(
        max_length=10,
        choices=[('PREMIUM', 'Premium'), ('AD_FREE', 'Ad Free')]
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'Active'),
            ('EXPIRED', 'Expired'),
            ('CANCELLED', 'Cancelled'),
            ('FAILED', 'Failed')
        ],
        default='ACTIVE'
    )
    expiry_date = models.DateTimeField()

    class Meta:
        db_table = 'purchase_history'