from django.contrib import admin
from django.utils.html import format_html


# Register your models here.

from .models import *



class HepsiAdmin(admin.ModelAdmin):
    list_display = ("title","Model", "youtube" ,"okunma_sayisi","seo_check","status","yayin_tarihi","guncelleme_tarihi","small_banner","banner","aktif",)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title",)
    list_filter = ("status","Model","aktif","banner","small_banner",)
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
            checks.append(format_html('<span style="color: red;">Title: Duplicate words found</span>'))
        else:
            checks.append(format_html('<span style="color: green;">Title: No duplicate words</span>'))

        # H1 duplicate words check
        h1_words = obj.h1.split(" ")  # Replace 'h1' with the actual field name for your H1
        if len(h1_words) != len(set(h1_words)):
            checks.append(format_html('<span style="color: red;">H1: Duplicate words found</span>'))
        else:
            checks.append(format_html('<span style="color: green;">H1: No duplicate words</span>'))

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