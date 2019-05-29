from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .basex import base_encode
from .forms import UrlForm
from .models import ShortLink


def home(request):

    def get_short_path_from_database(url):
        try:
            sl = ShortLink.objects.get(url=url)
            return sl.short_path
        except ShortLink.DoesNotExist:
            return None

    def generate_short_path_with_base_62(url):

        def get_next_id():
            try:
                return cache.incr('short_url_id')
            except ValueError:
                cache.set('short_url_id', 62 ** 2 - 1)  # we'll start with 3 symbol URLs
                return cache.incr('short_url_id')

        short_path = base_encode(get_next_id())
        ShortLink(url=url, short_path=short_path).save()
        return short_path

    def save_to_user_links(link):
        user_links = request.session.setdefault('user_links', [])
        user_links.insert(0, short_path)
        request.session.modified = True

    context = {}
    form = UrlForm()

    if request.method == 'POST':
        form = UrlForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['url']
            custom_path = form.cleaned_data['custom_path']

            if custom_path:
                ShortLink(url=url, short_path=custom_path).save()
                short_path = custom_path
            else:
                short_path = get_short_path_from_database(url)
                if not short_path:
                    short_path = generate_short_path_with_base_62(url)

            save_to_user_links(short_path)
            context['new_short_url'] = short_path
            form = UrlForm()  # clean the form after successful operation

    context['user_links'] = ShortLink.objects.filter(short_path__in=request.session.get('user_links', []))
    context['form'] = form
    return render(request, 'shortnr/home.html', context)


def redirect_to_full_url(request, short_path):
    full_url = cache.get(short_path)
    if full_url:
        return redirect(full_url)

    link = get_object_or_404(ShortLink, short_path=short_path)
    cache.set(short_path, link.url, 60 * 60 * 2)
    return redirect(link.url)
