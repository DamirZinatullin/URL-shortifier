import os
from datetime import datetime

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory, modelformset_factory

from django.http import Http404
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.generic import DetailView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from shortifier.services import *
from url_shortifier.settings import MEDIA_ROOT
from .forms import *
# Create your views here.
from .models import *
from .serializers import URLSerializer


def error_404_view(request, exception):
    return render(request, 'shortifier/404.html')


def index(request):
    '''Начальная страница'''

    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            try:
                url_model = URLModel.objects.get(source_url=form.cleaned_data.get('source_url'))
                to_slugify = form.cleaned_data.get('to_slugify')
                if to_slugify:
                    slug_url = SlugURLModel(slug_url=create_slug_url(to_slugify), source_url=url_model)
                    slug_url.save()
            except URLModel.DoesNotExist:
                url_model = form.save()
                url_model.short_url = create_short_url(url_model.pk)
                to_slugify = form.cleaned_data.get('to_slugify')
                if to_slugify:
                    slug_url = SlugURLModel(slug_url=create_slug_url(to_slugify), source_url=url_model)
                    slug_url.save()
            url_model.save()
            path = create_path_to_file(url_model.short_url.split('/')[-1] + '.png')
            create_qr_code(url_model.source_url, path)
            with open(path, 'rb') as f:
                url_model.qrcode.save((url_model.short_url.split('/')[-1] + '.png'), f)
            os.remove(path)

            return redirect(url_model)
        else:
            context = {'form': form}
            return render(request, 'shortifier/index.html', context=context)
    else:
        form = URLForm()
    context = {'form': form}
    return render(request, 'shortifier/index.html', context=context)


def contact(request):
    '''Страница обратной связи'''

    return render(request, 'shortifier/contact.html')


class URLDetailView(DetailView):
    '''Вывод сгенерированных коротких URL'''

    model = URLModel
    context_object_name = 'short_url'
    template_name = 'shortifier/url_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        source_url_form = OutputForm(instance=self.object)
        SlugUrlFormset = modelformset_factory(SlugURLModel, form=SlugURLForm, extra=0)
        formset = SlugUrlFormset(queryset=SlugURLModel.objects.filter(source_url=self.object.id))
        context['form'] = source_url_form
        context['formset'] = formset

        return context


class SearchSource(DetailView):
    '''Поиск исходного URL'''

    template_name = 'shortifier/url_detail.html'
    context_object_name = 'short_url'

    def get_object(self, queryset=None):
        model = URLModel.objects.filter(
            Q(short_url=self.request.GET.get('q')) | Q(slug_url__slug_url=self.request.GET.get('q'))).first()
        if not model:
            raise Http404('Такого URL не существует')
        return model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SourceUrlForm(instance=self.object)
        context['form'] = form
        return context


def redirect_to_source_url(request, slug):
    '''Перенаправление на URL исходного сайта'''

    url_model = URLModel.objects.filter(short_url=os.path.join(settings.ROOT_URL, slug)).first()
    if url_model:
        return redirect(to=url_model.source_url)
    url_model = SlugURLModel.objects.filter(slug_url=os.path.join(settings.ROOT_URL, slug)).first()
    if url_model:
        return redirect(to=url_model.source_url.source_url)
    else:
        raise Http404('Такого URL не существует')


class URLAPIView(APIView):
    '''Вывод URL адреса'''

    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        url_model = URLModel.objects.get(id=pk)
        serializer = URLSerializer(url_model)
        return Response(serializer.data)
