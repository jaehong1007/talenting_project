import io
from django.core.files import File
from django.test import TestCase

from member.models import User
from .models import Hosting, HostingReview, Photo

USER_EMAIL = 'user@gmail.com'
USER_PASSWORD = 'password'
HOST_EMAIL = 'host@gmail.com'
HOST_PASSWORD = 'password'
IMAGE = File(io.BytesIO())
PHOTO_NAME = 'My house'


def create_user(email, password):
    user = User.objects.create_user(
        email=email,
        password=password,
    )
    return user


def create_hosting(user):
    hosting = Hosting.objects.create(
        owner=user,
    )
    return hosting


def create_hosting_review(user, host, hosting):
    hosting_review = HostingReview.objects.create(
        author=user,
        host=host,
        hosting=hosting,
    )
    return hosting_review


def create_photo(hosting, image, name):
    photo = Photo.objects.create(
        place=hosting,
        image=image,
        name=name,
    )
    return photo


class HostingModelTest(TestCase):
    def test_saving_and_retrieving_hosting(self):
        user = create_user(USER_EMAIL, USER_PASSWORD)

        hosting = create_hosting(user)
        self.assertEqual(hosting.owner, user)
        self.assertEqual(hosting.title, '')
        self.assertEqual(hosting.description, '')
        self.assertEqual(hosting.to_do, '')
        self.assertEqual(hosting.rules, None)
        self.assertEqual(hosting.primary_photo, None)
        self.assertEqual(hosting.category, 1)
        self.assertEqual(hosting.house_type, 1)
        self.assertEqual(hosting.room_type, 1)
        self.assertEqual(hosting.capacity, 1)
        self.assertEqual(hosting.meal_type, 1)
        self.assertEqual(hosting.internet, 1)
        self.assertEqual(hosting.language, '')
        self.assertEqual(hosting.min_stay, 1)
        self.assertEqual(hosting.max_stay, 1)
        self.assertEqual(hosting.country, '')
        self.assertEqual(hosting.city, '')
        self.assertEqual(hosting.distinct, '')
        self.assertEqual(hosting.street, '')
        self.assertEqual(hosting.address, None)
        self.assertEqual(hosting.active, True)
        self.assertEqual(hosting.published, False)


class HostingReviewModelTest(TestCase):
    def test_saving_and_retrieving_hosting_review(self):
        user = create_user(USER_EMAIL, USER_PASSWORD)
        host = create_user(HOST_EMAIL, HOST_PASSWORD)
        hosting = create_hosting(host)
        hosting_review = create_hosting_review(user, host, hosting)

        self.assertEqual(hosting_review.author, user)
        self.assertEqual(hosting_review.host, host)
        self.assertEqual(hosting_review.hosting, hosting)
        self.assertEqual(hosting_review.text, '')
        self.assertEqual(hosting_review.recommend, True)


class PhotoModelTest(TestCase):
    def test_saving_and_retrieving_photo(self):
        host = create_user(HOST_EMAIL, HOST_PASSWORD)
        hosting = create_hosting(host)
        photo = create_photo(hosting, IMAGE, PHOTO_NAME)

        self.assertEqual(photo.place, hosting)
        self.assertEqual(photo.name, PHOTO_NAME)
        self.assertEqual(photo.image, IMAGE)
        self.assertEqual(photo.type, 5)
