from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password):

        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_active = True
        user.is_admin = True

        user.save(using=self.db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    is_host = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def write_review_to_guest(self, guest_pk, review, rating):
        '''
        :param guest_pk: 호스트 권한을 가진 유저가 게스트에게 리뷰를 남기는 메소드.
        :return: 리뷰가 새로 생성되었으면 True, 아니면 False
        '''
        if self.is_host and not self.user_review_about_guest.filter(host=self).exists():
            GuestReview.objects.create(
                host=self,
                guest=User.objects.get(pk=guest_pk),
                review=review,
                rating=rating
            )
            return True
        return False

    def get_guest_review_by_hosts(self):
        '''해당 게스트에게 호스트가 등록한 리뷰의 전체 리스트를 반환'''
        return self.user_review_about_guest.filter(guest=self)


class GuestReview(models.Model):
    '''호스트가 숙박한 게스트를 평가할 때 사용하는 모델'''
    host = models.ForeignKey(User, related_name='user_review_by_host')
    guest = models.ForeignKey(User, related_name='user_review_about_guest')
    review = models.TextField()
    rating = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
