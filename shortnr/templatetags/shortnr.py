from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def short_url(context, short_path):
    return context['request'].build_absolute_uri(
        reverse('short_url_redirect', kwargs={'short_path': short_path})
    )