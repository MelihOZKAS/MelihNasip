from django.contrib import admin
from django.utils.html import format_html


# Register your models here.

from .models import *



class HepsiAdmin(admin.ModelAdmin):
    list_display = ("title","Model","okunma_sayisi","description_length","status","yayin_tarihi","small_banner","banner","aktif",)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title",)
    list_filter = ("status","Model","aktif","banner","small_banner",)
    list_editable = ("status","aktif","banner","small_banner",)

    def seo_check(self, obj):
        checks = []

        # Title check
        title_length = len(obj.title)
        if 50 <= title_length <= 60:
            checks.append(format_html('<span style="color: green;">Title: {}/60</span>', title_length))
        else:
            checks.append(format_html('<span style="color: red;">Title: {}/60</span>', title_length))

        # H1 check
        h1_length = len(obj.h1)  # Replace 'h1' with the actual field name for your H1
        if 20 <= h1_length <= 70:
            checks.append(format_html('<span style="color: green;">H1: {}/70</span>', h1_length))
        else:
            checks.append(format_html('<span style="color: red;">H1: {}/70</span>', h1_length))

        # Keywords check
        keywords_length = len(obj.keywords)
        if 130 < keywords_length <= 155:
            checks.append(format_html('<span style="color: green;">Keywords: {}/155</span>', keywords_length))
        else:
            checks.append(format_html('<span style="color: red;">Keywords: {}/155</span>', keywords_length))

        # Meta description check
        meta_description_length = len(obj.meta_description)
        if 130 < meta_description_length <= 155:
            checks.append(
                format_html('<span style="color: green;">Meta Description: {}/155</span>', meta_description_length))
        else:
            checks.append(
                format_html('<span style="color: red;">Meta Description: {}/155</span>', meta_description_length))

        return format_html("<br>".join(checks))

    seo_check.short_description = 'SEO'




    #def description_length(self, obj):
    #    length = len(obj.meta_description)
    #    if 130 < length <= 155:
    #        return format_html('<span style="color: green;">{}/155</span>', length)
    #    else:
    #        return format_html('<span style="color: red;">{}/155</span>', length)
#
    #description_length.short_description = 'Desc-Len'

admin.site.register(SiirMasal, HepsiAdmin)


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