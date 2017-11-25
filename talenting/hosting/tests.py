import io
from django.core.files import File
from django.test import TestCase

from member.models import User
from .models import Hosting, HostingReview, Photo, Description, LocationInfo

# Dummy info
USER_EMAIL = 'user@gmail.com'
USER_PASSWORD = 'password'
HOST_EMAIL = 'host@gmail.com'
HOST_PASSWORD = 'password'
IMAGE = File(io.BytesIO())
PHOTO_NAME = 'My house'
FIRST_NAME = 'Andreea'
LAST_NAME = 'Sorian'


def create_user(email, password, first_name, last_name):
    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    return user


def create_hosting(user):
    hosting = Hosting.objects.create(owner=user)
    return hosting


def create_hosting_review(user, host, hosting):
    hosting_review = HostingReview.objects.create(author=user, host=host, place=hosting)
    return hosting_review


def create_photo(hosting, image, name):
    photo = Photo.objects.create(place=hosting, image=image, name=name)
    return photo


def create_description(hosting):
    description = Description.objects.create(place=hosting)
    return description


def create_location_info(hosting):
    location_info = LocationInfo.objects.create(place=hosting)
    return location_info


class HostingModelTest(TestCase):
    def test_saving_and_retrieving_hosting(self):
        user = create_user(USER_EMAIL, USER_PASSWORD, FIRST_NAME, LAST_NAME)
        hosting = create_hosting(user)

        self.assertEqual(hosting.owner, user)
        self.assertEqual(hosting.title, '')
        self.assertEqual(hosting.primary_photo, None)
        self.assertEqual(hosting.category, 1)
        self.assertEqual(hosting.house_type, 1)
        self.assertEqual(hosting.room_type, 1)
        self.assertEqual(hosting.capacity, 1)
        self.assertEqual(hosting.meal_type, 1)
        self.assertEqual(hosting.internet, 1)
        self.assertEqual(hosting.language, '')
        self.assertEqual(hosting.rules, '')
        self.assertEqual(hosting.min_stay, 1)
        self.assertEqual(hosting.max_stay, 1)
        self.assertEqual(hosting.country, '')
        self.assertEqual(hosting.city, '')
        self.assertEqual(hosting.distinct, '')
        self.assertEqual(hosting.street, '')
        self.assertEqual(hosting.address, '')
        self.assertEqual(hosting.postcode, '')
        self.assertEqual(hosting.active, True)
        self.assertEqual(hosting.published, False)


class HostingReviewModelTest(TestCase):
    def test_saving_and_retrieving_hosting_review(self):
        user = create_user(USER_EMAIL, USER_PASSWORD, FIRST_NAME, LAST_NAME)
        host = create_user(HOST_EMAIL, HOST_PASSWORD, FIRST_NAME, LAST_NAME)
        hosting = create_hosting(host)
        hosting_review = create_hosting_review(user, host, hosting)

        self.assertEqual(hosting_review.author, user)
        self.assertEqual(hosting_review.host, host)
        self.assertEqual(hosting_review.place, hosting)
        self.assertEqual(hosting_review.review, '')
        self.assertEqual(hosting_review.recommend, True)


class PhotoModelTest(TestCase):
    def test_saving_and_retrieving_photo(self):
        host = create_user(HOST_EMAIL, HOST_PASSWORD, FIRST_NAME, LAST_NAME)
        hosting = create_hosting(host)
        photo = create_photo(hosting, IMAGE, PHOTO_NAME)

        self.assertEqual(photo.place, hosting)
        self.assertEqual(photo.name, PHOTO_NAME)
        self.assertEqual(photo.image, IMAGE)
        self.assertEqual(photo.type, 1)


class DescriptionModelTest(TestCase):
    def test_saving_and_retrieving_description(self):
        host = create_user(HOST_EMAIL, HOST_PASSWORD, FIRST_NAME, LAST_NAME)
        hosting = create_hosting(host)
        description = create_description(hosting)

        self.assertEqual(description.place, hosting)
        self.assertEqual(description.title, '')
        self.assertEqual(description.description, '')
        self.assertEqual(description.to_do, '')


class LocationInfoTest(TestCase):
    def test_saving_and_retrieving_location_info(self):
        host = create_user(HOST_EMAIL, HOST_PASSWORD, FIRST_NAME, LAST_NAME)
        hosting = create_hosting(host)
        location_info = create_location_info(hosting)

        self.assertEqual(location_info.place, hosting)
        self.assertEqual(location_info.description, '')
        self.assertEqual(location_info.neighborhood, '')
