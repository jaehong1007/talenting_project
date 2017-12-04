from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.db import models

User = get_user_model()


class WishListItems(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='userself')
    wish_event = models.ForeignKey(settings.EVENT_ITEM_MODEL, related_name='wish_event')
    wish_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='wish_user')
    notes = models.TextField(blank=True, null=True)
    added_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    class Meta:
        verbose_name = 'wishlist'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-created_at']
        unique_together = ['user', 'wish_event'], ['user', 'wish_user']

    def __str__(self):
        return f'event_wishlist (' \


    def get_absolute_url(self):
        return self.wish_event.get_absolute_url()
