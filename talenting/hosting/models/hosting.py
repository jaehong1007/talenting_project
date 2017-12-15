from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from ..options import *

User = get_user_model()


class HostingManager(models.Model):
    def get_queryset(self):
        return super().get_queryset().exclude(owner=None)


class Hosting(models.Model):
    # Representation
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.SmallIntegerField(choices=CATEGORIES, default=1)
    title = models.CharField(max_length=50)
    summary = models.TextField(max_length=500)
    primary_photo = models.ImageField(blank=True)
    recommend_counter = models.IntegerField(blank=True, null=True)

    # House
    house_type = models.SmallIntegerField(choices=HOUSE_TYPES, default=1)
    room_type = models.SmallIntegerField(choices=ROOM_TYPES, default=1)
    meal_type = models.SmallIntegerField(choices=MEAL_TYPES, default=1)
    capacity = models.SmallIntegerField(choices=CAPACITIES, default=1)
    internet = models.SmallIntegerField(choices=INTERNET_TYPES, default=1)
    smoking = models.NullBooleanField()
    pet = models.NullBooleanField()
    rules = models.TextField(blank=True)
    language = ArrayField(models.CharField(max_length=5, choices=LANGUAGES))
    min_stay = models.SmallIntegerField(choices=MIN_STAY, default=1)
    max_stay = models.SmallIntegerField(choices=MAX_STAY, default=1)

    # Description
    description = models.TextField(blank=True)
    to_do = models.TextField(blank=True)
    exchange = models.TextField(blank=True)
    neighborhood = models.TextField(blank=True)
    transportation = models.TextField(blank=True)

    # Address
    country = models.CharField(max_length=2, choices=COUNTRIES, blank=True)
    city = models.CharField(max_length=10, blank=True)
    distinct = models.CharField(max_length=40, blank=True)
    street = models.CharField(max_length=60, blank=True)
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10, blank=True)

    # Geolocation
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)

    # Timestamp/Status
    has_photo = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_primary_photo(self):
        """
        primary_photo is used for representing list.
        The method is called when HostingPhoto object is created.
        """
        photos = self.hostingphoto_set.all()
        if photos:
            self.primary_photo = photos[0].hosting_thumbnail
            self.has_photo = True
            self.save()

    def get_photos(self):
        photos = self.hostingphoto_set.all()
        return photos

    def get_hosting_reviews(self):
        return self.hostingreview_set.all()

    def get_recommend_counter(self):
        reviews = self.hostingreview_set.all()
        count = 0
        for rev in reviews:
            if rev.recommend:
                count += 1
        self.recommend_counter = count

    def save(self, *args, **kwargs):
        self.get_recommend_counter()
        super(Hosting, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.owner.get_full_name()}'

    class Meta:
        ordering = ['-has_photo', '-recommend_counter']

    object = HostingManager()


class HostingPhoto(models.Model):
    place = models.ForeignKey(Hosting, on_delete=models.CASCADE)
    hosting_image = models.ImageField(upload_to='hosting', blank=True)
    hosting_thumbnail = ImageSpecField(source='hosting_image',
                                       processors=[ResizeToFit(767)],
                                       format='JPEG',
                                       options={'quality': 85})
    caption = models.CharField(max_length=50, blank=True)
    type = models.SmallIntegerField(choices=PHOTO_TYPES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Photo: {self.caption}({self.type})'

    def save(self, *args, **kwargs):
        super(HostingPhoto, self).save(*args, **kwargs)
        if self.place:
            self.place.get_primary_photo()

    class Meta:
        ordering = ['-created_at']


class HostingReview(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='author')
    host = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    place = models.ForeignKey(Hosting, null=True, on_delete=models.SET_NULL)
    hosting_review = models.TextField()
    recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Author: {self.author.first_name}'

    class Meta:
        ordering = ['-created_at']
