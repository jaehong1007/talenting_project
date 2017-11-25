import io
import unittest
from random import randint

from django.core.files import File

from member.models import User
from .models import Hosting, HostingReview, Photo, Description, LocationInfo


class HostingModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User(
            email='user@gmail.com',
            password='password',
            first_name='Namwoo',
            last_name='Seo',
        )
        cls.host = User(
            email='host@gmail.com',
            password='password',
            first_name='Andreea',
            last_name='Sorian',
        )
        cls.hosting = Hosting(owner=cls.host)

    def test_saving_and_retrieving_hosting(self):
        self.assertEqual(self.hosting.owner, self.host)
        self.assertEqual(self.hosting.title, '')
        self.assertEqual(self.hosting.primary_photo, None)
        self.assertEqual(self.hosting.category, 1)
        self.assertEqual(self.hosting.house_type, 1)
        self.assertEqual(self.hosting.room_type, 1)
        self.assertEqual(self.hosting.capacity, 1)
        self.assertEqual(self.hosting.meal_type, 1)
        self.assertEqual(self.hosting.internet, 1)
        self.assertEqual(self.hosting.language, '')
        self.assertEqual(self.hosting.rules, '')
        self.assertEqual(self.hosting.min_stay, 1)
        self.assertEqual(self.hosting.max_stay, 1)
        self.assertEqual(self.hosting.country, '')
        self.assertEqual(self.hosting.city, '')
        self.assertEqual(self.hosting.distinct, '')
        self.assertEqual(self.hosting.street, '')
        self.assertEqual(self.hosting.address, '')
        self.assertEqual(self.hosting.postcode, '')
        self.assertEqual(self.hosting.active, True)
        self.assertEqual(self.hosting.published, False)

    def test_saving_and_retrieving_hosting_review(self):
        hosting_review = HostingReview(author=self.user, host=self.host, place=self.hosting)

        self.assertEqual(hosting_review.author, self.user)
        self.assertEqual(hosting_review.host, self.host)
        self.assertEqual(hosting_review.place, self.hosting)
        self.assertEqual(hosting_review.review, '')
        self.assertEqual(hosting_review.recommend, True)

    def test_saving_and_retrieving_photo(self):
        image = File(io.BytesIO())
        photo_name = 'My house'

        photo = Photo(place=self.hosting, image=image, name=photo_name)

        self.assertEqual(photo.place, self.hosting)
        self.assertEqual(photo.name, photo_name)
        self.assertEqual(photo.image, image)
        self.assertEqual(photo.type, 1)

    def test_saving_and_retrieving_description(self):
        description = Description(place=self.hosting)

        self.assertEqual(description.place, self.hosting)
        self.assertEqual(description.title, '')
        self.assertEqual(description.description, '')
        self.assertEqual(description.to_do, '')

    def test_saving_and_retrieving_location_info(self):
        location_info = LocationInfo(place=self.hosting)

        self.assertEqual(location_info.place, self.hosting)
        self.assertEqual(location_info.description, '')
        self.assertEqual(location_info.neighborhood, '')


class HostingMethodTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            email='user@gmail.com',
            password='password',
            first_name='Namwoo',
            last_name='Seo',
        )
        cls.host = User.objects.create_user(
            email='host@gmail.com',
            password='password',
            first_name='Andreea',
            last_name='Sorian',
        )
        cls.hosting = Hosting.objects.create(owner=cls.host)

    def test_get_primary_photo_method(self):
        num = randint(0, 10)
        for i in range(num):
            Photo.objects.create(place=self.hosting)
        photos = self.hosting.photo_set.all()
        self.assertEqual(photos.count(), num)

        self.hosting.get_primary_photo()

        self.assertEqual(self.hosting.primary_photo, photos[0].image)

