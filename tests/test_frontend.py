from unittest.mock import patch
import pytest


@patch('shortnr.views.cache')
@pytest.mark.django_db
def test_create_short_url(cache, django_app_factory):
    import re
    from shortnr.basex import BASE_LIST
    from shortnr.models import ShortLink

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
