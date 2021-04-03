from django.contrib import admin
from .models import *


# Register your models here.


class URLModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_url', 'short_url', 'created_at', 'updated_at', 'qrcode')
    fields = ('source_url', 'short_url', 'qrcode')
    list_display_links = ('source_url', 'short_url')
    search_fields = ('source_url',)
    readonly_fields = ('short_url',)


admin.site.register(URLModel, URLModelAdmin)


class SlugURLModelAdmin(admin.ModelAdmin):
    list_display = ('slug_url', 'source_url')
    readonly_fields = ('source_url',)


admin.site.register(SlugURLModel, SlugURLModelAdmin)
