from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password, is_active=False, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self.db)
        return user_obj

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user

    def create_staff(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_admin=False,
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=120, blank=True, null=True, verbose_name=('name'))
    last_name = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
