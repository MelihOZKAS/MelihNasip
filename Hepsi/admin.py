from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.utils.safestring import mark_safe


# Register your models here.

from .models import *
from django.utils.text import slugify

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



class HepsiAdmin(admin.ModelAdmin):
    list_display = ("title","Model", "youtube" ,"okunma_sayisi","seo_check","status","kelime_sayisi","yayin_tarihi","olusturma_tarihi" ,"guncelleme_tarihi","small_banner","banner","aktif",)#"get_hikayeKategorisi", "get_masalKategorisi",
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title", "slug", "h1")
    list_filter = ("status","Model","aktif","banner","small_banner",)
    list_editable = ("status","aktif","banner","small_banner",)

    actions = ['update_slug','update_creation_date']



    #def get_hikayeKategorisi(self, obj):
    #    return ", ".join([hikaye.HikayeKategoriAdi for hikaye in obj.hikayeKategorisi.all()])
    #get_hikayeKategorisi.short_description = 'Hikaye Kategorileri'
#
    #def get_masalKategorisi(self, obj):
    #    return ", ".join([masal.MasalKategoriAdi for masal in obj.masalKategorisi.all()])
    #get_masalKategorisi.short_description = 'Masal Kategorileri'

    def update_slug(self, request, queryset):
        for obj in queryset:
            obj.title, obj.slug = create_unique_title_slug(obj.title)
            obj.save()

    update_slug.short_description = 'Slug değerlerini ve başlıkları title\'a göre güncelle'

    def update_creation_date(self, request, queryset):
        for obj in queryset:
            obj.olusturma_tarihi = timezone.now()
            obj.save()
    update_creation_date.short_description = 'Oluşturma tarihlerini güncelle.'

    def seo_check(self, obj):
        checks = []

        # Title check
        title_length = len(obj.title)
        if 50 <= title_length <= 60:
            checks.append(format_html('<span style="color: green;">Title: {}/50-60</span>', title_length))
        else:
            checks.append(format_html('<span style="color: red;">Title: {}/50-60</span>', title_length))

        # H1 check
        h1_length = len(obj.h1)  # Replace 'h1' with the actual field name for your H1
        if 20 <= h1_length <= 70:
            checks.append(format_html('<span style="color: green;">H1: {}/20-70</span>', h1_length))
        else:
            checks.append(format_html('<span style="color: red;">H1: {}/20-70</span>', h1_length))

        # Keywords check
        keywords = obj.keywords.split(",")
        keywords_length = len(keywords)
        if 5 <= keywords_length <= 15:  # Assuming you want between 1 and 10 keywords
            checks.append(format_html('<span style="color: green;">Keywords: {}/5-15</span>', keywords_length))
        else:
            checks.append(format_html('<span style="color: red;">Keywords: {}/5-15</span>', keywords_length))

        # Meta description check
        meta_description_length = len(obj.meta_description)
        if 130 < meta_description_length <= 155:
            checks.append(
                format_html('<span style="color: green;">Meta Description: {}/130-155</span>', meta_description_length))
        else:
            checks.append(
                format_html('<span style="color: red;">Meta Description: {}/130-155</span>', meta_description_length))

        title_words = obj.title.split(" ")
        if len(title_words) != len(set(title_words)):
            checks.append(format_html('<span style="color: red;">Title: Mükkerer kelimeler var</span>'))
        else:
            checks.append(format_html('<span style="color: green;">Title: Süpersin Hepsi Uniq</span>'))

        # H1 duplicate words check
        h1_words = obj.h1.split(" ")  # Replace 'h1' with the actual field name for your H1
        if len(h1_words) != len(set(h1_words)):
            checks.append(format_html('<span style="color: red;">H1: Mükkerer kelimeler var</span>'))
        else:
            checks.append(format_html('<span style="color: green;">H1: Süpersin Hepsi Uniq</span>'))

        return format_html("<br>".join(checks))

    seo_check.short_description = 'SEO'

admin.site.register(SiirMasal, HepsiAdmin)





class BlogAdmin(admin.ModelAdmin):
    list_display = ("title","youtube" ,"okunma_sayisi","seo_check","status","yayin_tarihi","guncelleme_tarihi","small_banner","banner","aktif",)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title",)
    list_filter = ("status","aktif","banner","small_banner",)
    list_editable = ("status","aktif","banner","small_banner",)



    def seo_check(self, obj):
        checks = []

        # Title check
        title_length = len(obj.title)
        if 50 <= title_length <= 60:
            checks.append(format_html('<span style="color: green;">Title: {}/50-60</span>', title_length))
        else:
            checks.append(format_html('<span style="color: red;">Title: {}/50-60</span>', title_length))

        # H1 check
        h1_length = len(obj.h1)  # Replace 'h1' with the actual field name for your H1
        if 20 <= h1_length <= 70:
            checks.append(format_html('<span style="color: green;">H1: {}/20-70</span>', h1_length))
        else:
            checks.append(format_html('<span style="color: red;">H1: {}/20-70</span>', h1_length))

        # Keywords check
        keywords = obj.keywords.split(",")
        keywords_length = len(keywords)
        if 5 <= keywords_length <= 15:  # Assuming you want between 1 and 10 keywords
            checks.append(format_html('<span style="color: green;">Keywords: {}/5-15</span>', keywords_length))
        else:
            checks.append(format_html('<span style="color: red;">Keywords: {}/5-15</span>', keywords_length))

        # Meta description check
        meta_description_length = len(obj.meta_description)
        if 130 < meta_description_length <= 155:
            checks.append(
                format_html('<span style="color: green;">Meta Description: {}/130-155</span>', meta_description_length))
        else:
            checks.append(
                format_html('<span style="color: red;">Meta Description: {}/130-155</span>', meta_description_length))

        title_words = obj.title.split(" ")
        if len(title_words) != len(set(title_words)):
            checks.append(format_html('<span style="color: red;">Title: Mükkerer kelimeler var</span>'))
        else:
            checks.append(format_html('<span style="color: green;">Title: Süpersin Hepsi Uniq</span>'))

        # H1 duplicate words check
        h1_words = obj.h1.split(" ")  # Replace 'h1' with the actual field name for your H1
        if len(h1_words) != len(set(h1_words)):
            checks.append(format_html('<span style="color: red;">H1: Mükkerer kelimeler var</span>'))
        else:
            checks.append(format_html('<span style="color: green;">H1: Süpersin Hepsi Uniq</span>'))

        return format_html("<br>".join(checks))

    seo_check.short_description = 'SEO'

admin.site.register(Blog, BlogAdmin)









class MasalAdmin(admin.ModelAdmin):
    list_display = ("MasalKategoriAdi","MasalSlug","sirasi","Masal_meta_description","description_length","Masal_keywords","Aktif","Banner",)
    prepopulated_fields = {'MasalSlug': ('MasalKategoriAdi',)}
    search_fields = ("MasalKategoriAdi",)
    list_filter = ("Aktif","Banner",)
    list_editable = ("Aktif","Banner","sirasi",)
    def description_length(self, obj):
        length = len(obj.Masal_meta_description)
        if length <= 155:
            return format_html('<span style="color: green;">{}/155</span>', length)
        else:
            return format_html('<span style="color: red;">{}/155</span>', length)
    description_length.short_description = 'Desc-Len'

admin.site.register(MasalKategorileri, MasalAdmin)


class HikayeAdmin(admin.ModelAdmin):
    list_display = ("HikayeKategoriAdi","HikayeSlug","sirasi","Hikaye_meta_description","description_length","Hikaye_keywords","Aktif","Banner",)
    prepopulated_fields = {'HikayeSlug': ('HikayeKategoriAdi',)}
    search_fields = ("HikayeKategoriAdi",)
    list_filter = ("Aktif","Banner",)
    list_editable = ("Aktif","Banner","sirasi")

    def description_length(self, obj):
        length = len(obj.Hikaye_meta_description)
        if length <= 155:
            return format_html('<span style="color: green;">{}/155</span>', length)
        else:
            return format_html('<span style="color: red;">{}/155</span>', length)
    description_length.short_description = 'Desc-Len'

admin.site.register(HikayeKategorileri, HikayeAdmin)


class iletisimAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(iletisimmodel, iletisimAdmin)


class hayvanAdmin(admin.ModelAdmin):
    list_display = ("ismi",)


admin.site.register(Animals, hayvanAdmin)

class oyunlarAdmin(admin.ModelAdmin):
    list_display = ("oyun_turu",)


admin.site.register(Oyunlar, oyunlarAdmin)


@admin.register(MobileUser)
class MobileUserAdmin(admin.ModelAdmin):
    list_display = (
    'user_photo', 'username', 'email', 'created_at', 'last_login', 'is_premium', 'is_ad_free', 'gold_balance',
    'last_login_platform')
    list_filter = ('is_premium', 'is_ad_free', 'last_login_platform')
    search_fields = ('username', 'email', 'google_id', 'apple_id')

    def user_photo(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo}" style="width: 30px; height: 30px; border-radius: 50%; object-fit: cover;" />')
        return 'No Photo'

    user_photo.short_description = 'Photo'

@admin.register(FavoriteStory)
class FavoriteStoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'added_date')
    list_filter = ('added_date',)
    search_fields = ('user__username', 'story__title')