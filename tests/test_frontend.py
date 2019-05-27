from unittest.mock import patch

from django.urls import reverse
from model_mommy import mommy
import pytest

from shortnr.models import ShortLink


@patch('shortnr.views.cache')
@pytest.mark.django_db
def test_create_short_url(cache, django_app_factory):
    import re
    from shortnr.basex import BASE_LIST

    client = django_app_factory(csrf_checks=False)

    # Given there're some short urls generated
    # that took all /xx (2 char) short urls
    cache.incr.return_value = len(BASE_LIST) ** 2

    long_url = (
        'https://www.quora.com/Are-long-URLs-bad-for-SEO-'
        'Does-the-length-of-the-URLs-do-more-harm-to-SEO-'
        'than-the-benefit-gained-by-including-good-content-in-the-URL'
    )

    # When user clicks 'Shorten' button
    resp = client.post('/', {'url': long_url})

    # Then there's a short link in the response
    short_link = resp.lxml.xpath('//input[@id="short-url"]/@value')[0]
    assert re.match(r'^http://testserver/[a-zA-Z0-9]{3}$', short_link)

    # and there's a record in the db
    sl = ShortLink.objects.get()
    assert sl.url == long_url
    assert sl.short_path == short_link.split('/')[-1]


@pytest.mark.django_db
def test_redirect_to_full_url(client):
    from shortnr.basex import base_encode

    # Given there's a short URL in the database
    link = mommy.make('ShortLink', url='https://www.google.com', short_path=base_encode(5555))

    # When user types a short URL in a browser
    resp = client.get(
        reverse('short_url_redirect', kwargs={'short_path': link.short_path})
    )

    # Then he's redirected to full URL
    assert resp.status_code == 302
    assert resp['Location'] == link.url