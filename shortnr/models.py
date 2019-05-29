from django.db import models


class ShortLink(models.Model):
    url = models.URLField(db_index=True)
    short_path = models.CharField(max_length=10, db_index=True, unique=True)
