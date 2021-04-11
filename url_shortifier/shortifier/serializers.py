import os

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shortifier.models import *
from shortifier.services import create_slug_url, create_short_url, create_path_to_file, create_qr_code


class SlugURLSerializer(ModelSerializer):
    # slug_url = serializers.SlugRelatedField(slug_field='slug_url', read_only=True)

    class Meta:
        model = SlugURLModel
        fields = ('slug_url',)


class URLSerializer(ModelSerializer):
    slug_url = SlugURLSerializer(read_only=True, many=True)

    class Meta:
        model = URLModel
        fields = ('source_url', 'short_url', 'slug_url')


class CreateShortURLSerializer(ModelSerializer):
    to_slugify = serializers.CharField(max_length=200, required=False)

    def create(self, validated_data):
        try:
            source_url = validated_data.get('source_url')
            url_model = URLModel.objects.get(source_url=source_url)
            to_slugify = validated_data.get('to_slugify')
            print(to_slugify)
            if to_slugify:
                slug_url = SlugURLModel(slug_url=create_slug_url(to_slugify), source_url=url_model)
                slug_url.save()
        except URLModel.DoesNotExist:
            url_model = URLModel(source_url=validated_data.get('source_url'))
            url_model.save()
            url_model.short_url = create_short_url(url_model.pk)
            to_slugify = validated_data.get('to_slugify')
            if to_slugify:
                slug_url = SlugURLModel(slug_url=create_slug_url(to_slugify), source_url=url_model)
                slug_url.save()
        url_model.save()
        path = create_path_to_file(url_model.short_url.split('/')[-1] + '.png')
        create_qr_code(url_model.source_url, path)
        with open(path, 'rb') as f:
            url_model.qrcode.save((url_model.short_url.split('/')[-1] + '.png'), f)
        os.remove(path)
        return url_model

    class Meta:
        model = URLModel
        fields = ('source_url', 'to_slugify')
