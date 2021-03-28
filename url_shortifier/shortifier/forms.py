import os

from django import forms
from django.core.exceptions import ValidationError

from url_shortifier import settings
from .models import *
from .services import slugify


class URLForm(forms.ModelForm):
    '''Форма URL адреса'''
    to_slugify = forms.CharField(max_length=200, label='Исходный текст для человекочитаемого URL (ЧПУ)', required=False,
                                 widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = URLModel
        fields = ('source_url', 'to_slugify', 'slug_url')
        widgets = {
            'source_url': forms.URLInput(attrs={"class": 'form-control'}),
            'to_slugify': forms.TextInput(attrs={"class": 'form-control'}),
            'slug_url': forms.URLInput(attrs={"class": 'form-control', 'disabled': True}),
        }

    def clean_to_slugify(self):
        to_slugify = self.cleaned_data.get('to_slugify')
        slug_url = os.path.join(settings.ROOT_URL, slugify(to_slugify))
        if URLModel.objects.filter(slug_url=slug_url).exists():
            raise ValidationError('Ссылка с таким ЧПУ уже существует, пожлуйста измените текст для ЧПУ')
        return to_slugify


class OutputForm(forms.ModelForm):
    class Meta:
        model = URLModel
        fields = ('short_url', 'slug_url')
        widgets = {
            'short_url': forms.TextInput(attrs={"class": 'form-control'}),
            'slug_url': forms.TextInput(attrs={"class": 'form-control'})}