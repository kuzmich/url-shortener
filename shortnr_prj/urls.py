from django.contrib import admin
from django.urls import path, re_path

from shortnr import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^(?P<short_path>[a-zA-Z0-9_-]+)$', views.redirect_to_full_url, name='short_url_redirect'),
    path('admin/', admin.site.urls),
]
