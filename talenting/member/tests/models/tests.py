import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ...models import User, Profile
import random
from django.conf import settings

ALPHABET_FOR_TEST = 'abcdefghijklmnopqrstuvwxyz'


def rand_name(len, char):
    return "".join([random.choice(char) for _ in range(len)])


def make_guest(email, password):
    user = User.objects.create_user(email=email, password=password,
                                    first_name=rand_name(5, ALPHABET_FOR_TEST),
                                    last_name=rand_name(5, ALPHABET_FOR_TEST))
    user.is_active = True
    user.save()
    return user


def make_host(email, password):
    user = make_guest(email=email, password=password)
    user.is_host = True
    user.save()
    return user


class UserModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_user = User()
        first_user.email = 'sejun12@gmail.com'
        first_user.password = 'ab33591242'
        first_user.first_name = rand_name(5, ALPHABET_FOR_TEST)
        first_user.last_name = rand_name(5, ALPHABET_FOR_TEST)
        first_user.save()

        second_user = User()
        second_user.email = 'sejun13@gmail.com'
        second_user.password = 'ab33591242'
        first_user.first_name = rand_name(5, ALPHABET_FOR_TEST)
        first_user.last_name = rand_name(5, ALPHABET_FOR_TEST)
        second_user.save()

        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 2)

        first_saved_user = saved_users[0]
        second_saved_user = saved_users[1]
        self.assertEqual(first_saved_user.email, 'sejun12@gmail.com')
        self.assertEqual(second_saved_user.email, 'sejun13@gmail.com')

    def test_custom_method_operations(self):
        superuser = User.objects.create_superuser(email='superuser@gmail.com', password='ab33591242',
                                                  first_name=rand_name(5, ALPHABET_FOR_TEST),
                                                  last_name=rand_name(5, ALPHABET_FOR_TEST))
        normal = User.objects.create_user(email='normal@gmail.com', password='ab33591242',
                                          first_name=rand_name(5, ALPHABET_FOR_TEST),
                                          last_name=rand_name(5, ALPHABET_FOR_TEST))

        self.assertEqual(superuser, User.objects.get(email='superuser@gmail.com'))
        self.assertEqual(normal, User.objects.get(email='normal@gmail.com'))

        self.assertTrue(superuser.is_staff, 'supseruser should have staff authorization')
        self.assertTrue(superuser.is_admin, 'supseruser should have admin authorization')

        self.assertFalse(normal.is_staff, 'normal user should not have staff authorizaiton')


class GuestReviewModelTest(TestCase):
    def test_host_can_review_the_guest(self):
        sejun = make_host(email='sejun@gmail.com', password='ab33591242')
        jaehong = make_host(email='jaehong@gmail.com', password='ab33591242')
        is_review_created = jaehong.write_review_to_guest(
            guest_pk=sejun.pk, review='세준씨는 좋은 사람입니다', recommend=False)
        self.assertTrue(is_review_created)

        sejun_review = sejun.get_guest_review_by_hosts()[0]
        self.assertEqual(sejun_review.host, jaehong)
        self.assertEqual(sejun_review.review, '세준씨는 좋은 사람입니다')

    def test_guest_review_can_show_multiple_reviews_in_descending_order_by_created_date(self):
        jaehong = make_host(email='jaehong@gmail.com', password='ab33591242')
        youngchan = make_host(email='youngchan@gmail.com', password='ab33591242')
        sejun = make_guest(email='sejun@gmail.com', password='ab33591242')
        jaehong.write_review_to_guest(guest_pk=sejun.pk, review='세준씨는 좋은 사람입니다', recommend=False)
        youngchan.write_review_to_guest(guest_pk=sejun.pk, review='세준씨는 좋은 사람입니다2', recommend=False)

        sejun_reviews = sejun.get_guest_review_by_hosts()
        self.assertEqual(len(sejun_reviews), 2)
        review_messages = ['세준씨는 좋은 사람입니다2', '세준씨는 좋은 사람입니다']
        for index, review in enumerate(sejun_reviews):
            self.assertEqual(review.review, review_messages[index])

    def test_guest_has_recomendation_number(self):
        jaehong = make_host(email='jaehong@gmail.com', password='ab33591242')
        youngchan = make_host(email='youngchan@gmail.com', password='ab33591242')
        sejun = make_guest(email='sejun@gmail.com', password='ab33591242')
        jaehong.write_review_to_guest(guest_pk=sejun.pk, review='세준씨는 좋은 사람입니다', recommend=True)
        youngchan.write_review_to_guest(guest_pk=sejun.pk, review='세준씨는 좋은 사람입니다2', recommend=True)
        sejun = User.objects.last()
        self.assertEqual(sejun.recommendations, 2)


class ProfileModelTest(TestCase):
    def test_user_has_a_profile(self):
        sejun = make_host(email='sejun@gmail.com', password='ab33591242')
        path = os.path.join(settings.STATIC_DIR, 'test', 'sejun_profile.jpg')
        photo = SimpleUploadedFile(name='test_image.jpg', content=open(path, 'rb').read(),
                                   content_type='image/jpeg')
        sejun_profile = Profile.objects.create(user=sejun, self_intro='나는 세준입니다', my_talent='영어 잘합니다',
                                               city='서울', occupation='학생', available_languages=['한국어', '영어'],
                                               profile_image=photo)
        self.assertEqual(sejun_profile.user, sejun)
        self.assertEqual(sejun_profile.available_languages, ['한국어', '영어'])
        sejun_profile.profile_image.delete()
