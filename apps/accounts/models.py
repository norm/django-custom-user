from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        now = timezone.now()
        email = UserManager.normalize_email(email)
        fields = {
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'email': email,
            'last_login': now,
            'date_joined': now,
        }
        fields.update(extra_fields)

        user = self.model(**fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(PermissionsMixin, AbstractBaseUser):
    """ Custom user class using email address for the username. """

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=512, blank=True, null=True)
    familiar_name = models.CharField(max_length=512, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.familiar_name

    @property
    def welcome_name(self):
        return self.familiar_name or self.full_name or self.email
