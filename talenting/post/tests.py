from django.test import TestCase

from member.models import User
from .models import Hosting


class HostingModelTest(TestCase):
    DUMMY_EMAIL = 'dummy@gmail.com'
    DUMMY_PASSWORD = 'password'

    def test_saving_and_retrieving_hosting(self):
        user = User.objects.create_user(
            email=self.DUMMY_EMAIL,
            password=self.DUMMY_PASSWORD,
        )
        hosting = Hosting(owner=user)
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
