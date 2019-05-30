import logging

from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from .basex import base_encode
from .forms import UrlForm
from .models import ShortLink, UserLink

logger = logging.getLogger(__name__)


def home(request):

    def get_short_link_from_database(url):
        try:
            return ShortLink.objects.get(url=url, custom=False)
        except ShortLink.DoesNotExist:
            return None

    def generate_short_link_with_base_62(url):

        def get_next_id():
            try:
                return cache.incr('short_url_id')
            except ValueError:
                cache.set('short_url_id', 62 ** 2 - 1, None)  # we'll start with 3 symbol URLs
                return cache.incr('short_url_id')

        short_path = base_encode(get_next_id())
        link = ShortLink(url=url, short_path=short_path)
        link.save()
        return link

    def save_to_user_links(link):
        user_links = request.session.setdefault('user_links', [])
        user_links.append(link.short_path)
        request.session.modified = True

        try:
            UserLink(session_id=request.session.session_key, link=link).save()
        except IntegrityError:  # if link is already appended to user's links
            pass

    def get_user_links():
        qs = ShortLink.objects.filter(userlink__session_id=request.session.session_key)\
                              .order_by('-userlink__created_at')
        paginator = Paginator(qs, 10)
        return paginator.get_page(request.GET.get('page'))

    context = {}
    form = UrlForm()

    if request.method == 'POST':
        form = UrlForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['url']
            custom_path = form.cleaned_data['custom_path']

            if custom_path:
                link = ShortLink(url=url, short_path=custom_path, custom=True)
                link.save()
            else:
                link = get_short_link_from_database(url)
                if not link:
                    link = generate_short_link_with_base_62(url)

            save_to_user_links(link)
            context['new_short_url'] = link.short_path
            form = UrlForm()  # clean the form after successful operation

    context['user_links'] = get_user_links()
    context['form'] = form
    return render(request, 'shortnr/home.html', context)


def redirect_to_full_url(request, short_path):
    full_url = cache.get(short_path)
    if full_url:
        return redirect(full_url)

    link = get_object_or_404(ShortLink, short_path=short_path)
    cache.set(short_path, link.url, 60 * 60 * 2)
    return redirect(link.url)
