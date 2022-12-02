from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import os


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


def image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "pfp_pid_%s.%s" % (instance.user.userprofile.id, ext)
    return os.path.join('profile_pics', filename)


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    NONBINARY = 'N'
    BOTH = 'B'

    gender_choices = [(MALE, 'Male'), (FEMALE, 'Female'),
                      (NONBINARY, 'NonBinary')]

    preference_choices = [(MALE, 'Male'), (FEMALE, 'Female'),
                          (NONBINARY, 'NonBinary'), (BOTH, 'Both')]

    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=1, choices=gender_choices, default=NONBINARY)
    preference = models.CharField(
        max_length=1, choices=preference_choices, default=BOTH)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    about = models.CharField(max_length=3000)
    image = models.ImageField(default='default.jpg', upload_to=image_path)
    blocklist = models.ManyToManyField(
        'UserProfile', related_name='blocked_by', through='BlockList', symmetrical=False, blank=False)
    chat_requests = models.ManyToManyField(
        'UserProfile', related_name='requests_received', through='ChatRequest', symmetrical=False, blank=False)
    reports = models.ManyToManyField(
        'UserProfile', related_name='reports_received', through='Reports', symmetrical=False, blank=False)

    def __str__(self):
        return self.user.email + ' profile'

    class Meta:
        ordering = ['first_name']


class BlockList(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    blocker = models.ForeignKey(
        UserProfile, related_name="user_blocking", on_delete=models.CASCADE)
    blocked = models.ForeignKey(
        UserProfile, related_name="user_blocked", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return self.blocker.user.email + " blocked " + self.blocked.user.email


class ChatRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=True)
    message = models.CharField(max_length=300, null=False, default='Hi')
    req_from = models.ForeignKey(
        UserProfile, related_name="user_from", on_delete=models.CASCADE)
    req_to = models.ForeignKey(
        UserProfile, related_name="user_to", on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=[(
        'A', 'Accepted'), ('D', 'Declined'), ('U', 'Unseen')], default='U', null=False)

    class Meta:
        unique_together = ('req_from', 'req_to')

    def __str__(self):
        return self.req_from.user.email + " requested " + self.req_to.user.email


class Reports(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=True)
    message = models.CharField(max_length=300, null=True)
    reporter = models.ForeignKey(
        UserProfile, related_name="report_by", on_delete=models.CASCADE)
    reported = models.ForeignKey(
        UserProfile, related_name="reported_user", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('reporter', 'reported')

    def __str__(self):
        return self.reporter.user.email + " reported " + self.reported.user.email
