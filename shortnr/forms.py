from django import forms
from .models import ShortLink


class UrlForm(forms.Form):
    url = forms.URLField(label='Type URL to shorten')
    custom_path = forms.SlugField(required=False, max_length=25, label='Optional short link custom ending')

    def clean_custom_path(self):
        data = self.cleaned_data['custom_path']

        if data:
            if ShortLink.objects.filter(short_path=data).exists():
                raise forms.ValidationError("This ending is already used.")

        return data