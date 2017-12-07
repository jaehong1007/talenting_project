import io
from django.core.files import File
from django.urls import resolve
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from hosting.models.hosting import Hosting
from member.models import User


class HostingListViewTest(APITestCase):
    # Resolved URL and URL name doesn't exactly match, it needs to be fixed.
    URL_API_HOSTING_LIST_NAME = 'api:hosting:hosting-list'
    URL_API_HOSTING_LIST = '/hosting/'

    @staticmethod
    def create_user():
        return User.objects.create_user(
            email='host2@gmail.com',
            password='password',
            first_name='Tonya',
            last_name='Ushakova',
        )

    @staticmethod
    def create_hosting(owner):
        return Hosting.objects.create(owner=owner)

    def test_hosting_list_url_name_reverse(self):
        url = reverse(self.URL_API_HOSTING_LIST_NAME)
        self.assertEqual(url, self.URL_API_HOSTING_LIST)

    def test_hosting_list_url_resolver(self):
        # Resolved URL and URL name doesn't exactly match.
        resolver_match = resolve(self.URL_API_HOSTING_LIST)
        self.assertEqual(resolver_match.url_name, self.URL_API_HOSTING_LIST_NAME)

    def test_get_hosting_list(self):
        user = self.create_user()
        self.create_hosting(owner=user)
        url = reverse(self.URL_API_HOSTING_LIST_NAME)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Response.data has three length of dictionary.
        self.assertEqual(len(response.data), 3)
        self.assertEqual(Hosting.objects.count(), 1)

        hosting_data = response.data['hosting'][0]
        self.assertIn('pk', hosting_data)
        self.assertIn('owner', hosting_data)
        self.assertIn('category', hosting_data)
        self.assertIn('title', hosting_data)
        self.assertIn('summary', hosting_data)
        self.assertIn('primary_photo', hosting_data)
        self.assertIn('recommend_counter', hosting_data)
        self.assertIn('house_type', hosting_data)
        self.assertIn('room_type', hosting_data)
        self.assertIn('meal_type', hosting_data)
        self.assertIn('capacity', hosting_data)
        self.assertIn('internet', hosting_data)
        self.assertIn('smoking', hosting_data)
        self.assertIn('pet', hosting_data)
        self.assertIn('rules', hosting_data)
        self.assertIn('language', hosting_data)
        self.assertIn('min_stay', hosting_data)
        self.assertIn('max_stay', hosting_data)
        self.assertIn('description', hosting_data)
        self.assertIn('to_do', hosting_data)
        self.assertIn('exchange', hosting_data)
        self.assertIn('neighborhood', hosting_data)
        self.assertIn('transportation', hosting_data)
        self.assertIn('country', hosting_data)
        self.assertIn('city', hosting_data)
        self.assertIn('distinct', hosting_data)
        self.assertIn('street', hosting_data)
        self.assertIn('address', hosting_data)
        self.assertIn('postcode', hosting_data)
        self.assertIn('min_lat', hosting_data)
        self.assertIn('max_lat', hosting_data)
        self.assertIn('min_lon', hosting_data)
        self.assertIn('max_lon', hosting_data)
        self.assertIn('has_photo', hosting_data)
        self.assertIn('published', hosting_data)
        self.assertIn('created_at', hosting_data)
        self.assertIn('updated_at', hosting_data)

    def test_create_hosting(self):
        host = self.create_user()
        self.client.force_authenticate(user=host)
        response = self.client.post('/hosting/', {
            'title': 'test',
            'summary': 'test',
            'country': 'GB',
            'city': 'London',
            'distinct': 'Kensington',
            'street': 'Victoria',
            'language': 'en'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hosting.objects.count(), 1)
        hosting_data = Hosting.objects.get(owner=host)

        self.assertEqual(hosting_data.title, 'test')
        self.assertEqual(hosting_data.summary, 'test')
        self.assertEqual(hosting_data.country, 'GB')
        self.assertEqual(hosting_data.city, 'London')
        self.assertEqual(hosting_data.distinct, 'Kensington')
        self.assertEqual(hosting_data.street, 'Victoria')
        self.assertEqual(hosting_data.language, 'en')


class HostingDetailViewTest(APITestCase):
    URL_API_HOSTING_DETAIL_NAME = 'api:hosting:hosting-detail'
    URL_API_HOSTING_DETAIL = '/hosting/1/'

    @staticmethod
    def create_user():
        return User.objects.create_user(
            email='host2@gmail.com',
            password='password',
            first_name='Tonya',
            last_name='Ushakova',
        )

    @staticmethod
    def create_hosting(owner):
        return Hosting.objects.create(owner=owner)

    def test_hosting_detail_url_name_reverse(self):
        url = reverse(self.URL_API_HOSTING_DETAIL_NAME, kwargs={'hosting_pk': 1})
        self.assertEqual(url, self.URL_API_HOSTING_DETAIL)

    def test_hosting_detail_url_resolver(self):
        resolver_match = resolve(self.URL_API_HOSTING_DETAIL)
        self.assertEqual(resolver_match.url_name, self.URL_API_HOSTING_DETAIL_NAME)

    def test_get_hosting_detail(self):
        user = self.create_user()
        self.create_hosting(owner=user)
        hosting_pk = Hosting.objects.get(owner=user).pk
        url = reverse(self.URL_API_HOSTING_DETAIL_NAME, kwargs={'hosting_pk': hosting_pk})
        response = self.client.get(url)

        # Test status code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test data length. Response.data has three length of dictionary.
        self.assertEqual(len(response.data), 3)
        # Test a number of hosting obejct.
        self.assertEqual(Hosting.objects.count(), 1)
        # Test specific data in hosting.
        hosting_data = response.data['hosting']
        self.assertIn('pk', hosting_data)
        self.assertIn('owner', hosting_data)
        self.assertIn('category', hosting_data)
        self.assertIn('title', hosting_data)
        self.assertIn('summary', hosting_data)
        self.assertIn('primary_photo', hosting_data)
        self.assertIn('recommend_counter', hosting_data)
        self.assertIn('house_type', hosting_data)
        self.assertIn('room_type', hosting_data)
        self.assertIn('meal_type', hosting_data)
        self.assertIn('capacity', hosting_data)
        self.assertIn('internet', hosting_data)
        self.assertIn('smoking', hosting_data)
        self.assertIn('pet', hosting_data)
        self.assertIn('rules', hosting_data)
        self.assertIn('language', hosting_data)
        self.assertIn('min_stay', hosting_data)
        self.assertIn('max_stay', hosting_data)
        self.assertIn('description', hosting_data)
        self.assertIn('to_do', hosting_data)
        self.assertIn('exchange', hosting_data)
        self.assertIn('neighborhood', hosting_data)
        self.assertIn('transportation', hosting_data)
        self.assertIn('country', hosting_data)
        self.assertIn('city', hosting_data)
        self.assertIn('distinct', hosting_data)
        self.assertIn('street', hosting_data)
        self.assertIn('address', hosting_data)
        self.assertIn('postcode', hosting_data)
        self.assertIn('min_lat', hosting_data)
        self.assertIn('max_lat', hosting_data)
        self.assertIn('min_lon', hosting_data)
        self.assertIn('max_lon', hosting_data)
        self.assertIn('has_photo', hosting_data)
        self.assertIn('published', hosting_data)
        self.assertIn('created_at', hosting_data)
        self.assertIn('updated_at', hosting_data)

        # Test specific data in code and msg.
        code = response.data['code']
        self.assertEqual(code, 200)
        msg = response.data['msg']
        self.assertEqual(msg, '')

    def test_update_hosting(self):
        user = self.create_user()
        self.create_hosting(owner=user)
        hosting_pk = Hosting.objects.get(owner=user).pk
        self.client.force_authenticate(user=user)
        response = self.client.put(f'/hosting/{hosting_pk}/', {
            'title': 'Seoul life',
            'summary': 'Seoul is cool city',
            'country': 'KR',
            'city': 'Seoul',
            'distinct': 'Gangnam',
            'street': 'Sinsa',
            'language': 'ko'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        hosting_data = Hosting.objects.get(owner=user)
        self.assertEqual(hosting_data.title, 'Seoul life')
        self.assertEqual(hosting_data.summary, 'Seoul is cool city')
        self.assertEqual(hosting_data.country, 'KR')
        self.assertEqual(hosting_data.city, 'Seoul')
        self.assertEqual(hosting_data.distinct, 'Gangnam')
        self.assertEqual(hosting_data.street, 'Sinsa')
        self.assertEqual(hosting_data.language, 'ko')

    def test_delete_hosting(self):
        user = self.create_user()
        self.create_hosting(owner=user)
        hosting_pk = Hosting.objects.get(owner=user).pk
        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/hosting/{hosting_pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
