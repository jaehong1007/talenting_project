from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.db import models


User = get_user_model()


class WishListItems(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    wish_event = models.ForeignKey(settings.EVENT_ITEM_MODEL)
    objects = UserManager()

    class Meta:
        verbose_name = 'wishlist'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-created_at']
        unique_together = ['user', 'wish_event']

    def __str__(self):
        return f'event_wishlist (' \
                f'{self.wish_event})'

    def __unicode__(self):
        assert self.wish_event

    def get_absolute_url(self):
        return self.wish_event.get_absolute_url()




