from django.contrib import admin
from .models import *


# Register your models here.


class URLModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_url', 'short_url', 'slug_url', 'created_at', 'updated_at')
    fields = ('source_url', 'short_url', 'slug_url')
    list_display_links = ('source_url', 'short_url', 'slug_url')
    search_fields = ('source_url',)
    readonly_fields = ('short_url',)


admin.site.register(URLModel, URLModelAdmin)
