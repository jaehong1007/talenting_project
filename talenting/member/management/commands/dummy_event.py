from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
import pytz
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
import mock
from django.core.files import File
file_mock = mock.MagicMock(spec=File, name='FileMock')
import tempfile
from event.models import Event

User = get_user_model()
seoul_tz = pytz.timezone("Asia/Seoul")
image_path = 'https://upload.wikimedia.org/wikipedia/commons/b/' \
             'b8/Seoul_Cheonggyecheon_night.jpg'


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(1, 16):
            host = User.objects.get(email=f'host{i}@gmail.com')
            Event.objects.create(
                author=host,
                event_categories=1,
                title=f"Host {i}'s Event",
                program=f"Let's have fun with host no.{i}",
                noted_item="This is dummy dummy dummy",
                country='KR',
                state='idw',
                city='seoul',
                primary_photo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                closing_date=seoul_tz.localize(datetime(2017, 12, 17, 17, 00)),
                event_date=seoul_tz.localize(datetime(2017, 12, 14, 17, 00)),
                maximum_participant=10,
            )
