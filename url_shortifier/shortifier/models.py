from django.db import models

# Create your models here.
from django.urls import reverse_lazy


class URLModel(models.Model):
    '''URL адреса:'''
    source_url = models.URLField(max_length=2083, verbose_name='Исходный url')
    short_url = models.URLField(max_length=100, unique=True, verbose_name='Укороченный url', null=True, db_index=True)
    slug_url = models.SlugField(unique=True, verbose_name='Человекочитаемый URL', blank=True, null=True, db_index=True, max_length=255)
    qrcode = models.ImageField(upload_to='qrcodes/%Y/%m/%d/', verbose_name='QR код')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'URL страницы'
        verbose_name_plural = 'URL-ы страниц'
        ordering = ['updated_at']

    def __str__(self):
        return self.source_url

    def get_absolute_url(self):
        return reverse_lazy('url_detail', kwargs={'pk': self.pk})
