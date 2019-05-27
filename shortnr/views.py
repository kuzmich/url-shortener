from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .basex import base_encode
from .models import ShortLink


def home(request):
    def is_valid_url(url):
        if len(url) <= 2000 \
           and (url.startswith('http://') or url.startswith('https://')):
            return True

        return False

    def get_short_url_from_cache(url):
        pass

    def get_short_url_from_database(url):
        try:
            sl = ShortLink.objects.get(url=url)
            return request.build_absolute_uri(sl.short_path)
        except ShortLink.DoesNotExist:
            return None

    def generate_short_url_with_base_62(url):

        def get_next_id():
            try:
                return cache.incr('short_url_id')
            except ValueError:
                cache.set('short_url_id', 62 ** 2 - 1)  # we'll start with 3 symbol URLs
                return cache.incr('short_url_id')

        short_path = base_encode(get_next_id())
        ShortLink(url=url, short_path=short_path).save()

        return request.build_absolute_uri(
            reverse('short_url_redirect', kwargs={'short_path': short_path})
        )

    if request.method == 'POST':
        url = request.POST['url']

        if not is_valid_url(url):
            pass

        short_url = get_short_url_from_cache(url)

        if not short_url:
            short_url = get_short_url_from_database(url)

        if not short_url:
            short_url = generate_short_url_with_base_62(url)

        return render(request, 'shortnr/url.html', {'short_url': short_url})

    else:
        return render(request, 'shortnr/home.html')


def redirect_to_full_url(request, short_path):
    link = get_object_or_404(ShortLink, short_path=short_path)
    return redirect(link.url)
