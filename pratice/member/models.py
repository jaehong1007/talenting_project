from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_GOOGLE = 'g'
    CHOICES_USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_DJANGO, 'Google'),
    )
    user_type = models.CharField(
        max_length=1,
        choices=CHOICES_USER_TYPE
    )
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='user',
        blank=True)
    age = models.IntegerField('나이')
    like_posts = models.ManyToManyField(
        'post.Post',
        related_name='like_users',
        blank=True,
        verbose_name='좋아요 누른 포스트 목록'
    )