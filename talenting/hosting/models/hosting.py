from django.conf import settings
from django.db import models

from ..options import *

User = settings.AUTH_USER_MODEL


class Hosting(models.Model):
    # Representation
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.SmallIntegerField(choices=CATEGORIES, default=1)
    title = models.CharField(max_length=50)
    summary = models.TextField(max_length=500)
    primary_photo = models.ImageField(upload_to='hosting', blank=True)

    # House
    house_type = models.SmallIntegerField(choices=HOUSE_TYPES, default=1)
    room_type = models.SmallIntegerField(choices=ROOM_TYPES, default=1)
    meal_type = models.SmallIntegerField(choices=MEAL_TYPES, default=1)
    capacity = models.SmallIntegerField(choices=CAPACITIES, default=1)
    internet = models.SmallIntegerField(choices=INTERNET_TYPES, default=1)
    smoking = models.NullBooleanField()
    pet = models.NullBooleanField()
    rules = models.TextField(blank=True)
    language = models.CharField(max_length=5, choices=LANGUAGES)
    min_stay = models.SmallIntegerField(choices=MIN_STAY, default=1)
    max_stay = models.SmallIntegerField(choices=MAX_STAY, default=1)

    # Address
    country = models.CharField(max_length=2, choices=COUNTRIES)
    city = models.CharField(max_length=10)
    distinct = models.CharField(max_length=40)
    street = models.CharField(max_length=60)
    address = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=10, blank=True)

    # Timestamp/Status
    active = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_primary_photo(self):
        photos = self.photo_set.all()
        if photos:
            self.primary_photo = photos[0].image
            self.save()

    def get_hosting_reviews(self):
        return self.hostingreview_set.all()

    def __str__(self):
        return self.title


class Photo(models.Model):
    place = models.ForeignKey(Hosting, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hosting')
    caption = models.CharField(max_length=50, blank=True)
    type = models.SmallIntegerField(choices=PHOTO_TYPES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Photo: {self.caption}({self.type})'


class Description(models.Model):
    place = models.OneToOneField(Hosting, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    to_do = models.TextField(blank=True)
    exchange = models.TextField(blank=True)
    neighborhood = models.TextField(blank=True)
    transportation = models.TextField(blank=True)

    def __str__(self):
        return f'Description: {self.place.title}'


class HostingReview(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='author')
    host = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    place = models.ForeignKey(Hosting, null=True, on_delete=models.SET_NULL)
    review = models.TextField()
    recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Author: {self.author.first_name}'

    class Meta:
        ordering = ['-created_at']


class GeoLocation(models.Model):
    place = models.OneToOneField(Hosting, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f'Location: {self.place.title}'
