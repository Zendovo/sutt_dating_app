from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_moderator(self, email, password, **other_fields):

        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_moderator', True)

        if other_fields.get('is_moderator') is not True:
            raise ValueError(
                'Moderator must be assigned to is_moderator=True.')

        return self.create_user(email, password, **other_fields)



class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = None
    first_name = None
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_moderator = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    age = models.IntegerField()
    first_name = models.CharField(max_length=100, blank=False)    
    last_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.email