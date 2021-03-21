from django.conf.urls.static import static
from django.urls import path, include

from shortifier.views import *

urlpatterns = [
    path('', index, name='index'),
    path('short_url/<int:pk>/', URLDetailView.as_view(), name='url_detail'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/short_url/<int:pk>/', URLAPIView.as_view(), name='url_api_detail'),
    path('<str:slug>', redirect_to_source_url, name='redirect_to_source_url')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
