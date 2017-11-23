from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from post.countries import COUNTRIES


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Event(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    title = models.CharField(max_length=20)
    program = models.TextField(max_length=300, blank=True)
    noted_item = models.TextField(max_length=100, blank=True, null=True)
    country = models.CharField(_('Country'), max_length=2, choices=COUNTRIES)
    state = models.CharField(_('State/Region'), max_length=40, null=True, blank=True)
    city = models.CharField(_('City'), max_length=40)
    price = models.DecimalField(_('Price per person'), decimal_places=2, max_digits=6, blank=True, null=True)
    photo = models.ImageField(upload_to='post')
    starting_date = models.DateTimeField(null=True)
    closing_date = models.DateTimeField(null=True)
    maximum_participant = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = EventManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Evenet (PK: {self.pk})'


class EventComment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    event = models.ForeignKey(Event, related_name='comments')
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

