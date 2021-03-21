import os
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render, redirect, get_list_or_404
from django.views.generic import DetailView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from shortifier.services import *
from url_shortifier.settings import MEDIA_ROOT
from .forms import URLForm, OutputForm
# Create your views here.
from .models import URLModel
from .serializers import URLSerializer


def index(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            try:
                url_model = URLModel.objects.get(source_url=form.cleaned_data.get('source_url'))
                to_slugify = form.cleaned_data.get('to_slugify')
                if to_slugify:
                    url_model.slug_url = create_slug_url(to_slugify)
            except URLModel.DoesNotExist:
                url_model = form.save()
                url_model.short_url = create_short_url(url_model.pk)
                to_slugify = form.cleaned_data.get('to_slugify')
                if to_slugify:
                    url_model.slug_url = create_slug_url(to_slugify)
            url_model.save()
            path = create_path_to_file(url_model.short_url.split('/')[-1]+'.png')
            create_qr_code(url_model.source_url, path)
            with open(path, 'rb') as f:
                url_model.qrcode.save((url_model.short_url.split('/')[-1]+'.png'), f)
            os.remove(path)

            return redirect(url_model)
    else:
        form = URLForm()
    context = {'form': form}
    return render(request, 'shortifier/index.html', context=context)


class URLDetailView(DetailView):
    model = URLModel
    context_object_name = 'short_url'
    template_name = 'shortifier/url_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = OutputForm(instance=self.object)
        context['form'] = form
        return context


def redirect_to_source_url(request, slug):
    queryset = get_list_or_404(URLModel, Q(short_url=settings.HOST_NAME + slug) |
                               Q(slug_url=settings.HOST_NAME + slug))
    url_model = queryset[0]
    return redirect(to=url_model.source_url)


class URLAPIView(APIView):
    '''Вывод URL адреса'''

    # permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        url_model = URLModel.objects.get(id=pk)
        serializer = URLSerializer(url_model)
        return Response(serializer.data)
