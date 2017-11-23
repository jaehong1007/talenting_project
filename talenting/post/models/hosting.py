from django.conf import settings
from django.db import models

from ..options import *

User = settings.AUTH_USER_MODEL


class Hosting(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    to_do = models.TextField()
    rules = models.TextField(blank=True, null=True)
    primary_photo = models.ImageField(upload_to='hosting', blank=True, null=True)
    category = models.SmallIntegerField(choices=CATEGORIES, default=1)

    house_type = models.SmallIntegerField(choices=HOUSE_TYPES, default=1)
    room_type = models.SmallIntegerField(choices=ROOM_TYPES, default=1)
    capacity = models.SmallIntegerField(choices=CAPACITIES, default=1)
    meal_type = models.SmallIntegerField(choices=MEAL_TYPES, default=1)
    internet = models.SmallIntegerField(choices=INTERNET_TYPES, default=1)
    language = models.CharField(max_length=5, choices=LANGUAGES)
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


class HostingReview(models.Model):
    author = models.ForeignKey(User, related_name='who_reviews')
    host = models.ForeignKey(User, related_name='who_is_reviewed', on_delete=models.CASCADE)
    hosting = models.ForeignKey(Hosting, related_name='where_is_reviewed')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
