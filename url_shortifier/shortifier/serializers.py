from rest_framework.serializers import ModelSerializer

from shortifier.models import URLModel


class URLSerializer(ModelSerializer):

    class Meta:
        model = URLModel
        fields = '__all__'
        title = 'djdjd'