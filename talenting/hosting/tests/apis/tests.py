import io
from django.core.files import File
from django.urls import resolve
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from hosting.models.hosting import Hosting
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


class HostingListViewTest(APITestCase):
    # Resolved URL and URL name doesn't exactly match, it needs to be fixed.
    URL_API_HOSTING_LIST_NAME = 'api:hosting:hosting-list'
    URL_API_HOSTING_LIST = '/hosting/'

    def test_hosting_list_url_name_reverse(self):
        url = reverse(self.URL_API_HOSTING_LIST_NAME)
        self.assertEqual(url, self.URL_API_HOSTING_LIST)

    def test_hosting_list_url_resolver(self):
        # Resolved URL and URL name doesn't exactly match.
        resolver_match = resolve(self.URL_API_HOSTING_LIST)
        self.assertEqual(resolver_match.url_name, self.URL_API_HOSTING_LIST_NAME)

    def test_get_hosting_list(self):
        host = make_user()
        hosting = make_hosting(host)
        url = reverse(self.URL_API_HOSTING_LIST_NAME)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(Hosting.objects.count(), 1)

    def test_create_hosting(self):
        host = make_user()
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
        self.assertEqual(len(response.data), 3)
        self.assertEqual(Hosting.objects.count(), 1)


class HostingDetailViewTest(APITestCase):
    URL_API_HOSTING_DETAIL_NAME = 'api:hosting:hosting-detail'
    URL_API_HOSTING_DETAIL = '/hosting/1/'

    def test_hosting_detail_url_name_reverse(self):
        url = reverse(self.URL_API_HOSTING_DETAIL_NAME, kwargs={'hosting_pk': 1})
        self.assertEqual(url, self.URL_API_HOSTING_DETAIL)

    def test_hosting_detail_url_resolver(self):
        resolver_match = resolve(self.URL_API_HOSTING_DETAIL)
        self.assertEqual(resolver_match.url_name, self.URL_API_HOSTING_DETAIL_NAME)

    def test_get_hosting_detail(self):
        host = make_user()
        hosting = make_hosting(host)
        url = reverse(self.URL_API_HOSTING_DETAIL_NAME, kwargs={'hosting_pk': hosting.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(Hosting.objects.count(), 1)

    def test_update_hosting(self):
        host = make_user()
        hosting = make_hosting(host)
        self.client.force_authenticate(user=host)
        response = self.client.put(f'/hosting/{hosting.pk}/', {
            'title': 'Seoul life',
            'summary': 'Seoul is cool city',
            'country': 'KR',
            'city': 'Seoul',
            'distinct': 'Gangnam',
            'street': 'Sinsa',
            'language': 'ko'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_hosting(self):
        host = make_user()
        hosting = make_hosting(host)
        self.client.force_authenticate(user=host)
        response = self.client.delete(f'/hosting/{hosting.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

