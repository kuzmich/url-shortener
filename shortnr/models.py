from django.contrib.sessions.models import Session
from django.db import models


class ShortLink(models.Model):
    url = models.URLField(db_index=True)
    short_path = models.CharField(max_length=25, db_index=True, unique=True)
    custom = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '/{} -> {}'.format(
            self.short_path,
            self.url if len(self.url) <= 50 else '{}...{}'.format(self.url[:25], self.url[-25:])
        )


class UserLink(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    link = models.ForeignKey(ShortLink, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['session', 'link'], name='unique_link_per_session')
        ]
