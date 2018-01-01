from datetime import timezone

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from config import settings
from .. import options
from .. import countries
from utils import deletion

User = get_user_model()


class HostingManager(models.Model):
    """
    Override get_queryset to filter hosting object without owner.
    """

    def get_queryset(self):
        return super().get_queryset().exclude(owner=None)


class Hosting(models.Model):
    """
    Representation.
        A user can only one hosting object.
        primary_photo take hosting_thumbnail from HostingPhoto model, it would use for representing hosting list.
        hosting_thumbnail refer to ./media/CACHE/image/hosting.

    House.
        To input multiple language from user, ArrayField in Postgres is applied.

    Address.
        address field would take a whole address of a user from Google map API.

    Geolocation.
        Value of latitude and longitude is utilized to show hostings around a user.
    """

    # Representation
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    category = models.SmallIntegerField(choices=options.CATEGORIES, default=1)
    title = models.CharField(max_length=50)
    summary = models.TextField(max_length=500)
    primary_photo = models.ImageField(blank=True)
    recommend_counter = models.IntegerField(blank=True, null=True)

    # House
    house_type = models.SmallIntegerField(choices=options.HOUSE_TYPES, default=1)
    room_type = models.SmallIntegerField(choices=options.ROOM_TYPES, default=1)
    meal_type = models.SmallIntegerField(choices=options.MEAL_TYPES, default=1)
    capacity = models.SmallIntegerField(choices=options.CAPACITIES, default=1)
    internet = models.SmallIntegerField(choices=options.INTERNET_TYPES, default=1)
    smoking = models.NullBooleanField()
    pet = models.NullBooleanField()
    rules = models.TextField(blank=True)
    language = ArrayField(models.CharField(max_length=5, choices=countries.LANGUAGES))
    min_stay = models.SmallIntegerField(choices=options.MIN_STAY, default=1)
    max_stay = models.SmallIntegerField(choices=options.MAX_STAY, default=1)

    # Description
    description = models.TextField(blank=True)
    to_do = models.TextField(blank=True)
    exchange = models.TextField(blank=True)
    neighborhood = models.TextField(blank=True)
    transportation = models.TextField(blank=True)

    # Address
    country = models.CharField(max_length=2, choices=countries.COUNTRIES, blank=True)
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

    def get_hosting_photos(self):
        return self.hostingphoto_set.all()  # return HostingPhoto queryset

    def get_hosting_reviews(self):
        return self.hostingreview_set.all()  # return HostingReview queryset

    def get_primary_photo(self):
        """
        Take queryset from HostingPhoto,
        and assign the first hosting_thumbnail in the queryset to primary_photo.
        """
        photos = self.get_hosting_photos()
        if photos:
            self.primary_photo = photos[0].hosting_thumbnail.open()
            self.has_photo = True
            self.save()

    @receiver([post_delete, post_save], sender='hosting.HostingReview')
    def get_recommend_counter(sender, instance, **kwargs):
        """
        This method executes when HostingReview object save and delete.
        """
        reviews = instance.place.get_hosting_reviews()  # instance is a HostingReview object.
        count = 0
        for rev in reviews:
            if rev.recommend:
                count += 1
        instance.place.recommend_counter = count
        instance.place.save()

    @receiver([post_delete, post_save], sender='hosting.Hosting')
    def is_host(sender, instance, **kwargs):
        """
        If a user have a hositng object, is_user property is Ture.
        Otherwise, False.
        """
        if Hosting.objects.filter(pk=instance.owner.pk).exists():  # instance is a Hosting object.
            instance.owner.is_host = True
        else:
            instance.owner.is_host = False
        instance.owner.save()

    def __str__(self):
        return f'{self.owner.get_short_name()}'

    class Meta:
        ordering = ['has_photo', '-recommend_counter']

    object = HostingManager()


class HostingPhoto(models.Model):
    place = models.ForeignKey(Hosting, on_delete=models.CASCADE)
    hosting_image = models.ImageField(upload_to='hosting', blank=True)
    # thumbnail is stored in .media/CACHE/images folder
    hosting_thumbnail = ImageSpecField(source='hosting_image',
                                       processors=[ResizeToFit(767)],
                                       format='JPEG',
                                       options={'quality': 85})
    caption = models.CharField(max_length=50, blank=True)
    type = models.SmallIntegerField(choices=options.PHOTO_TYPES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(HostingPhoto, self).save(*args, **kwargs)
        if self.place:
            self.place.get_primary_photo()

    def __str__(self):
        return f'Photo: {self.caption}({self.type})'

    class Meta:
        ordering = ['-created_at']


class HostingReview(models.Model):
    author = models.ForeignKey(User,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='author')
    host = models.ForeignKey(User,
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name='host')
    place = models.ForeignKey(Hosting,
                              null=True,
                              on_delete=models.SET_NULL)
    hosting_review = models.TextField()
    recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.first_name}'

    def is_editable(self):
        """
        After update period ends, user doesn't allow to update and delete hosting review.
        """
        period_end = self.created_at + timezone.timedelta(
            seconds=getattr(settings, 'REVIEW_UPDATE_PERIOD'))  # 2 days of review update period.
        if timezone.now() > period_end:
            return False
        return True

    class Meta:
        ordering = ['-created_at']


class HostingRequest(models.Model):
    """
    User send request to stay to host.

    * All fields are required.
    """
    # When user delete account, assign sentinel user.
    user = models.ForeignKey(User,
                             null=True,
                             on_delete=models.SET(deletion.get_sentinel_user),
                             related_name='sender')
    host = models.ForeignKey(User,
                             null=True,
                             on_delete=models.SET(deletion.get_sentinel_user),
                             related_name='receiver')
    place = models.ForeignKey(Hosting)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    number_travelers = models.IntegerField()
    description = models.TextField()
    accepted = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.get_short_name()}'

    @receiver([post_delete], sender=User)
    def ensure_request_status(sender, instance, **kwargs):
        """
        When a user who have sent a request to stay delete account,
        automatically that request become unaccepted and canceled.
        """
        instance.accepted = False
        instance.canceled = True
        instance.save()
