import io

from PIL.Image import Image
from django.core.files import File
from django.urls import resolve
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


def make_user():
    return mommy.make('member.User')


def make_hosting():
    return mommy.make('hosting.Hosting')


def make_hosting_review():
    return mommy.make('hosting.HostingReview')


def make_hosting_photo():
    return mommy.make('hosting.Photo')


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
        make_hosting()
        url = reverse(self.URL_API_HOSTING_LIST_NAME)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

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


class HostingDetailViewTest(APITestCase):
    URL_API_HOSTING_DETAIL_NAME = 'api:hosting:hosting-detail'

    def test_hosting_detail_url_name_reverse(self):
        hosting = make_hosting()
        url = reverse(self.URL_API_HOSTING_DETAIL_NAME, kwargs={'hosting_pk': hosting.pk})
        self.assertEqual(url, f'/hosting/{hosting.pk}/')

    def test_hosting_detail_url_resolver(self):
        hosting = make_hosting()
        resolver_match = resolve(f'/hosting/{hosting.pk}/')
        self.assertEqual(resolver_match.url_name, self.URL_API_HOSTING_DETAIL_NAME)

    def test_get_hosting_detail(self):
        hosting = make_hosting()
        url = reverse(self.URL_API_HOSTING_DETAIL_NAME, kwargs={'hosting_pk': hosting.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_update_hosting(self):
        hosting = make_hosting()
        self.client.force_authenticate(user=hosting.owner)
        response = self.client.put(f'/hosting/{hosting.pk}/', {
            'title': 'Seoul life',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['hosting']['title'], 'Seoul life')

    def test_delete_hosting(self):
        hosting = make_hosting()
        self.client.force_authenticate(user=hosting.owner)
        response = self.client.delete(f'/hosting/{hosting.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PhotoListViewTest(APITestCase):
    URL_API_PHOTO_LIST_NAME = 'api:hosting:photo-list'

    def test_photo_list_url_name_reverse(self):
        url = reverse(self.URL_API_PHOTO_LIST_NAME, kwargs={'hosting_pk': self.hosting.pk})
        self.assertEqual(url, f'/hosting/{hosting.pk}/photo/')

    def test_photo_list_url_resolver(self):
        hosting = make_hosting()
        make_hosting_photo()
        resolver_match = resolve(f'/hosting/{hosting.pk}/photo/')
        self.assertEqual(resolver_match.url_name, self.URL_API_PHOTO_LIST_NAME)

    def test_get_photo_list(self):
        hosting = make_hosting()
        make_hosting_photo()
        url = reverse(self.URL_API_PHOTO_LIST_NAME, kwargs={'hosting_pk': hosting.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_photo(self):
        hosting = make_hosting()
        file = io.BytesIO()
        self.client.force_authenticate(user=hosting.owner)
        response = self.client.post(f'/hosting/{hosting.pk}/photo/', {
            'hosting_image': file,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
