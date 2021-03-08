import hashids
import re

from shortifier.models import URLModel
from url_shortifier import settings


def create_short_url(url_id: int) -> str:
    hashid = hashids.Hashids(min_length=7)
    short_url = settings.HOST_NAME + hashid.encode(url_id)
    return short_url


def create_slug_url(to_slugify: str) -> str:
    slug_url = settings.HOST_NAME + slugify(to_slugify)
    return slug_url


def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


def save_slug_url(url_model: URLModel, form_cleaned_data=dict) -> None:
    to_slugify = form_cleaned_data.get('to_slugify')
    if to_slugify:
        url_model.slug_url = settings.HOST_NAME + slugify(to_slugify)
        url_model.save()
