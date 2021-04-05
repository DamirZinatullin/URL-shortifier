from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shortifier.models import *


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
