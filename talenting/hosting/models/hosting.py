from django.conf import settings
from django.db import models

from ..options import *

User = settings.AUTH_USER_MODEL


class Hosting(models.Model):
    owner = models.ForeignKey(User)
    category = models.SmallIntegerField(choices=CATEGORIES, default=1)
    title = models.CharField(max_length=100)
    summary = models.TextField(default='')
    primary_photo = models.ImageField(upload_to='hosting', blank=True, null=True)

    house_type = models.SmallIntegerField(choices=HOUSE_TYPES, default=1)
    room_type = models.SmallIntegerField(choices=ROOM_TYPES, default=1)
    capacity = models.SmallIntegerField(choices=CAPACITIES, default=1)
    meal_type = models.SmallIntegerField(choices=MEAL_TYPES, default=1)
    internet = models.SmallIntegerField(choices=INTERNET_TYPES, default=1)
    language = models.CharField(max_length=5, choices=LANGUAGES)
    rules = models.TextField(blank=True, null=True)
    min_stay = models.SmallIntegerField(choices=MIN_STAY, default=1)
    max_stay = models.SmallIntegerField(choices=MAX_STAY, default=1)

    country = models.CharField(max_length=2, choices=COUNTRIES)
    city = models.CharField(max_length=10)
    distinct = models.CharField(max_length=40)
    street = models.CharField(max_length=60)
    address = models.CharField(max_length=100, blank=True, null=True)

    active = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Photo(models.Model):
    place = models.ForeignKey(Hosting, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='hosting')
    type = models.SmallIntegerField(choices=PHOTO_TYPES, default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Description(models.Model):
    place = models.ForeignKey(Hosting)
    title = models.CharField(max_length=100)
    description = models.TextField()
    to_do = models.TextField()

    def __str__(self):
        return self.title


class HostingReview(models.Model):
    author = models.ForeignKey(User, related_name='who_reviews')
    host = models.ForeignKey(User, related_name='who_is_reviewed')
    place = models.ForeignKey(Hosting, related_name='where_is_reviewed')
    review = models.TextField()
    recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Author: {self.author.first_name}'

    class Meta:
        ordering = ['-created_at']


class LocationInfo(models.Model):
    place = models.ForeignKey(Hosting)
    description = models.TextField()
    neighborhood = models.TextField()

    def __str__(self):
        return f'Place: {self.place.title}'
