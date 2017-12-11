import io
import unittest
from random import randint

from django.core.files import File

from model_mommy import mommy

from hosting.models.hosting import Photo, Hosting, HostingReview
from member.models import User


def make_user():
    return mommy.make('member.User')


def make_hosting(user):
    return mommy.make('hosting.Hosting', owner=user)


def make_hosting_review(user, host, hosting):
    return mommy.make(
        'hosting.HostingReview',
        author=user,
        host=host,
        place=hosting,
    )


def make_hosting_photo(hosting, image):
    return mommy.make(
        'hosting.Photo',
        place=hosting,
        hosting_image=image,
    )


class HostingModelTest(unittest.TestCase):
    def test_saving_and_retrieving_hosting(self):
        host = make_user()
        hosting = make_hosting(host)
        self.assertEqual(hosting.owner, host)

    def test_saving_and_retrieving_hosting_review(self):
        user = make_user()
        host = make_user()
        hosting = make_hosting(host)
        review = make_hosting_review(user, host, hosting)

        self.assertEqual(review.author, user)
        self.assertEqual(review.host, host)
        self.assertEqual(review.place, hosting)

    def test_saving_and_retrieving_photo(self):
        host = make_user()
        hosting = make_hosting(host)
        image = File(io.BytesIO())
        photo = make_hosting_photo(hosting, image)

        self.assertEqual(photo.place, hosting)
        self.assertEqual(photo.hosting_image, image)

    def test_get_primary_photo_method(self):
        host = User.objects.create_user(
            email='garson1362@gmail.com',
            password='password',
            first_name='Namwoo',
            last_name='Seo',
        )
        hosting = Hosting.objects.create(owner=host)

        # Create random number of photo object in a hosting.
        num = randint(0, 10)
        for i in range(num):
            Photo.objects.create(place=hosting)
        photos = hosting.photo_set.all()  # Get all photos linked with a hosting.
        hosting.get_primary_photo()

        # Check the number of created photos and primary_photo.
        self.assertEqual(photos.count(), num)
        self.assertEqual(hosting.primary_photo, photos[0].hosting_image)

    # def test_get_recommend_counter_method(self):
    #     user = User.objects.create_user(
    #         email='Andreea@gmail.com',
    #         password='password',
    #         first_name='Andreea',
    #         last_name='Sorian',
    #     )
    #     host = User.objects.get(email='garson1362@gmail.com')
    #     hosting = Hosting.objects.get(owner=host)
    #
    #     num = randint(0, 10)
    #     for i in range(num):
    #         HostingReview.objects.create(
    #             author=user,
    #             host=host,
    #             place=hosting,
    #         )
    #     hosting.get_recommend_counter()
    #
    #     # Check the number of recommend.
    #     self.assertEqual(hosting.recommend_counter, num)