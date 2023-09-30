from django.contrib import admin

# Register your models here.

from .models import *

class HepsiAdmin(admin.ModelAdmin):
    list_display = ("title","Model","okunma_sayisi","youtube","status","yayin_tarihi","small_banner","banner","aktif")
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title",)
    list_filter = ("status","Model","aktif","banner","small_banner",)
    list_editable = ("status","aktif","banner","small_banner",)

admin.site.register(SiirMasal, HepsiAdmin)


class MasalAdmin(admin.ModelAdmin):
    list_display = ("MasalKategoriAdi","MasalSlug","sirasi","Masal_meta_description","Masal_keywords","Aktif","Banner",)
    prepopulated_fields = {'MasalSlug': ('MasalKategoriAdi',)}
    search_fields = ("MasalKategoriAdi",)
    list_filter = ("Aktif","Banner",)
    list_editable = ("Aktif","Banner","sirasi",)

admin.site.register(MasalKategorileri, MasalAdmin)


class HikayeAdmin(admin.ModelAdmin):
    list_display = ("HikayeKategoriAdi","HikayeSlug","sirasi","Hikaye_meta_description","Hikaye_keywords","Aktif","Banner",)
    prepopulated_fields = {'HikayeSlug': ('HikayeKategoriAdi',)}
    search_fields = ("HikayeKategoriAdi",)
    list_filter = ("Aktif","Banner",)
    list_editable = ("Aktif","Banner","sirasi")

admin.site.register(HikayeKategorileri, HikayeAdmin)