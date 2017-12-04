from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models
from rest_framework.authtoken.models import Token


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email=email, password=password,
                                first_name=first_name, last_name=last_name)
        user.is_active = True
        user.is_admin = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    # 기본 인증정보
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    recommendations = models.IntegerField(default=0)

    # 권한
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_host = models.BooleanField(default=False)
    # TimeStamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 유저의 추가정보

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def token(self):
        return Token.objects.get_or_create(user=self)[0].key

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

    def write_review_to_guest(self, guest_pk, review, recommend):
        '''
        호스트 권한을 가진 유저가 게스트에게 리뷰를 남기는 메소드.
        :return: 리뷰가 새로 생성되었으면 True, 아니면 False
        '''
        if self.is_host and not self.user_review_about_guest.filter(host=self).exists():
            guest = User.objects.get(pk=guest_pk)
            GuestReview.objects.create(
                host=self,
                guest=guest,
                review=review,
                recommend=recommend
            )
            if recommend:
                guest.recommendations += 1
                guest.save()
            return True
        return False

    def get_guest_review_by_hosts(self):
        '''해당 게스트에게 호스트가 등록한 리뷰의 전체 리스트를 반환'''
        return self.user_review_about_guest.filter(guest=self)

        # def get_user_average_rating(self):
        #     '''유저 레이팅의 평균을 소수점으로 반환'''
        #     user_reviews = self.user_review_about_guest.filter(guest=self)
        #     if user_reviews:
        #         user_ratings = [review.rating for review in user_reviews]
        #         return float("{0:.1f}".format(sum(user_ratings) / len(user_reviews)))
        #     return float(0)
        #

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True)
    self_intro = models.TextField(blank=True)
    talent_category = models.CharField(max_length=20, blank=True)
    talent_intro = models.TextField(blank=True)
    country = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    occupation = models.CharField(max_length=20, blank=True)
    available_languages = ArrayField(models.CharField(max_length=30, blank=True), null=True)

    @property
    def age(self):
        if self.birth:
            return self.calculate_age()
        else: return None

    def calculate_age(self):
        today = date.today()
        delta = relativedelta(today, self.birth)
        return str(delta.years)

class ProfileImage(models.Model):
    profile = models.ForeignKey('Profile', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile', null=False )
    created_at = models.DateTimeField(auto_now_add=True)


class GuestReview(models.Model):
    '''호스트가 숙박한 게스트를 평가할 때 사용하는 모델'''
    host = models.ForeignKey(User, related_name='user_review_by_host', on_delete=models.CASCADE)
    guest = models.ForeignKey(User, related_name='user_review_about_guest', on_delete=models.CASCADE)
    review = models.TextField()
    recommend = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
