from django.conf.urls.static import static
from django.urls import path, include
from shortifier.views import *

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('search/', SearchSource.as_view(), name='search'),
    path('short_url/<int:pk>/', URLDetailView.as_view(), name='url_detail'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/short_url/<int:pk>/', URLAPIView.as_view(), name='url_api_detail'),
    path('api/v1/short_url/create/', CreateShortURLAPI.as_view(), name='create_url_api'),
    path('<str:slug>', redirect_to_source_url, name='redirect_to_source_url')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
