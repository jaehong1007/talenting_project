from datetime import datetime

import mock
import pytz
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management import BaseCommand

from member.models import Profile, ProfileImage

file_mock = mock.MagicMock(spec=File, name='FileMock')

User = get_user_model()
seoul_tz = pytz.timezone("Asia/Seoul")
image_path = '/home/sejun/Desktop/isihara.jpg'


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin = User.objects.create_superuser(email=f'admin@gmail.com',
                                              password='1q2w3e4r5t',
                                              first_name='admin',
                                              last_name='admin')
        Profile.objects.create(user=admin)

        for i in range(1, 21):
            guest = User.objects.create_user(email=f'guest{i}@gmail.com',
                                             password='1q2w3e4r5t',
                                             first_name=f'guestfirst{i}',
                                             last_name=f'guestlast{i}')
            guest.is_active = True
            guest.is_host = False
            guest.save()
            guest_profile = Profile.objects.create(
                user=guest,
                birth=seoul_tz.localize(datetime(1991, 12, 17, 17, 00)),
                gender='male',
                self_intro=f'my name is sejun and this is test profile guest no.{i}',
                talent_category=('{art}'),
                talent_intro='who cares',
                country='kr',
                city='seoul',
                occupation='student',
                available_languages=('{ko, en}')
            )

        for i in range(1, 31):
            host = User.objects.create_user(email=f'host{i}@gmail.com',
                                            password='1q2w3e4r5t',
                                            first_name=f'hostfirst{i}',
                                            last_name=f'hostlast{i}')
            host.is_active = True
            host.is_host = True
            host.save()

            host_profile = Profile.objects.create(
                user=host,
                birth=seoul_tz.localize(datetime(1991, 12, 17, 17, 00)),
                gender='male',
                self_intro=f'my name is sejun and this is test profile host no.{i}',
                talent_category=('{art}'),
                talent_intro='who cares',
                country='kr',
                city='seoul',
                occupation='student',
                available_languages=('{ko, en}')
            )