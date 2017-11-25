from django.conf import settings
from django.db import models

from ..options import *

User = settings.AUTH_USER_MODEL


class Hosting(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.SmallIntegerField(choices=CATEGORIES, default=1)
    title = models.CharField(max_length=100)
    summary = models.TextField()
    primary_photo = models.ImageField(upload_to='hosting', blank=True, null=True)

    house_type = models.SmallIntegerField(choices=HOUSE_TYPES, default=1)
    room_type = models.SmallIntegerField(choices=ROOM_TYPES, default=1)
    capacity = models.SmallIntegerField(choices=CAPACITIES, default=1)
    meal_type = models.SmallIntegerField(choices=MEAL_TYPES, default=1)
    internet = models.SmallIntegerField(choices=INTERNET_TYPES, default=1)
    language = models.CharField(max_length=5, choices=LANGUAGES)
    rules = models.TextField(blank=True)
    min_stay = models.SmallIntegerField(choices=MIN_STAY, default=1)
    max_stay = models.SmallIntegerField(choices=MAX_STAY, default=1)

    country = models.CharField(max_length=2, choices=COUNTRIES)
    city = models.CharField(max_length=10)
    distinct = models.CharField(max_length=40)
    street = models.CharField(max_length=60)
    address = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=10, blank=True)

    active = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_primary_photo(self):
        photos = self.photo_set.all()
        if photos:
            self.primary_photo = photos[0].image
            self.save()

    def __str__(self):
        return self.title


class Photo(models.Model):
    place = models.ForeignKey(Hosting, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='hosting')
    type = models.SmallIntegerField(choices=PHOTO_TYPES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Description(models.Model):
    place = models.OneToOneField(Hosting, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    to_do = models.TextField()

    def __str__(self):
        return self.title


class HostingReview(models.Model):
    author = models.ForeignKey(User, related_name='who_reviews', on_delete=models.PROTECT)
    host = models.ForeignKey(User, related_name='who_is_reviewed', on_delete=models.PROTECT)
    place = models.ForeignKey(Hosting, related_name='where_is_reviewed', on_delete=models.PROTECT)
    review = models.TextField()
    recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Author: {self.author.first_name}'

    class Meta:
        ordering = ['-created_at']


class LocationInfo(models.Model):
    place = models.OneToOneField(Hosting, on_delete=models.CASCADE)
    description = models.TextField()
    neighborhood = models.TextField(blank=True)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)

    def __str__(self):
        return f'Place: {self.place.title}'
