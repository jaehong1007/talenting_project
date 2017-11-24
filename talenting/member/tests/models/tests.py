from django.test import TestCase
from ...models import User


def make_host(email, password):
    user = User.objects.create_user(email=email, password=password)
    user.is_host = True
    user.is_active = True
    user.save()
    return user


def make_guest(email, password):
    user = User.objects.create_user(email=email, password=password)
    user.is_active = True
    user.save()
    return user


class UserModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_user = User()
        first_user.email = 'sejun12@gmail.com'
        first_user.password = 'ab33591242'
        first_user.save()

        second_user = User()
        second_user.email = 'sejun13@gmail.com'
        second_user.password = 'ab33591242'
        second_user.save()

        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 2)

        first_saved_user = saved_users[0]
        second_saved_user = saved_users[1]
        self.assertEqual(first_saved_user.email, 'sejun12@gmail.com')
        self.assertEqual(second_saved_user.email, 'sejun13@gmail.com')

    def test_custom_method_operations(self):
        superuser = User.objects.create_superuser(email='superuser@gmail.com', password='ab33591242')
        normal = User.objects.create_user(email='normal@gmail.com', password='ab33591242')

        self.assertEqual(superuser, User.objects.get(email='superuser@gmail.com'))
        self.assertEqual(normal, User.objects.get(email='normal@gmail.com'))

        self.assertTrue(superuser.is_staff, 'supseruser should have staff authorization')
        self.assertTrue(superuser.is_admin, 'supseruser should have admin authorization')

        self.assertFalse(normal.is_staff, 'normal user should not have staff authorizaiton')


class GuestReviewModelTest(TestCase):
    def test_host_can_review_the_guest(self):
        jaehong = make_host(email='jaehong@gmail.com', password='ab33591242')
        sejun = make_guest(email='sejun@gmail.com', password='ab33591242')
        is_review_created = jaehong.write_review_to_guest(
            guest_pk=sejun.pk, review='세준씨는 좋은 사람입니다',rating=4)
        self.assertTrue(is_review_created)

        sejun_review = sejun.get_guest_review_by_hosts()[0]
        self.assertEqual(sejun_review.host, jaehong)
        self.assertEqual(sejun_review.review, '세준씨는 좋은 사람입니다')
