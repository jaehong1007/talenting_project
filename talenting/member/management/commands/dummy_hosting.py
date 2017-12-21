import mock
from django.core.files import File

file_mock = mock.MagicMock(spec=File, name='FileMock')

import pytz
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from hosting.models.hosting import Hosting

User = get_user_model()
seoul_tz = pytz.timezone("Asia/Seoul")
image_path = '/home/sejun/Desktop/test_image.jpg'


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(16, 31):
            host = User.objects.get(email=f'host{i}@gmail.com')
            Hosting.objects.create(
                owner=host,
                title=f'Hosting by test host no.{i}',
                summary=f'with host{i}, you will have a good time here',
                rules='no specific rules applied here',
                language=('{ko, en}'),
                description='you need to help me with the job',
                to_do='computer programming',
                exchange='instead I will teach you korean',
                neighborhood='holy shit',
                transportation='bus, train, subway, whatever',
                country='KR',
                address='3333'
            )
