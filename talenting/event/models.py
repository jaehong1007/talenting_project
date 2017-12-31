from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill, ResizeToFit

from event.options import EVENT_CATEGORIES
from .countries import COUNTRIES


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Event(models.Model):
    # Content
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=1)
    event_categories = models.SmallIntegerField(_('categories'), choices=EVENT_CATEGORIES, default=1)
    title = models.CharField(max_length=20)
    program = models.TextField(max_length=300, blank=True)
    noted_item = models.TextField(max_length=100, blank=True, null=True)

    # Location
    country = models.CharField(max_length=2, choices=COUNTRIES, blank=True)
    city = models.CharField(max_length=10, blank=True)
    distinct = models.CharField(max_length=40, blank=True)
    street = models.CharField(max_length=60, blank=True)
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10, blank=True)

    # etc
    price = models.DecimalField(_('Price per person'), decimal_places=2, max_digits=6, blank=True, null=True)

    # Date
    opening_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Participants
    participants = models.ManyToManyField(
        'member.User',
        related_name='participants',
        blank=True,
        verbose_name='참여한 유저 목록'
    )
    maximum_participant = models.IntegerField(blank=True, null=True, default=0)
    participants_count = models.IntegerField(default=0, editable=False, blank=True)

    # Geo Location
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)

    # Primary Photo
    primary_photo = models.ImageField(blank=True)

    objects = EventManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title}'

    def get_photos(self):
        photos = self.eventphoto_set.all()
        return photos

    def get_comments(self):
        comments = self.eventcomment_set.all()
        return comments

    def get_primary_photo(self):
        photos = self.get_photos()
        if photos:
            self.primary_photo = photos[0].image_thumbnail
            self.save()

    @property
    def participants_counter(self):
        return self.participants.count

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)


class EventComment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    events = models.ForeignKey(Event, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        super(EventComment, self).save(*args, **kwargs)


class EventPhoto(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    events = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFit(767)],
                                     format='JPEG',
                                     options={'quality': 85}
                                     )

    def save(self, *args, **kwargs):
        super(EventPhoto, self).save(*args, **kwargs)
        if self.events:
            self.events.get_primary_photo()
