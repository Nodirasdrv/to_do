from django.db import models

import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=255, unique=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True
        ordering = ['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""

        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractEmailUser):

    USER_TYPE_CHOICES = (
        ('owner', 'Owner'),
        ('reader', 'Reader'),
    )
    user_type = models.CharField(
        choices=USER_TYPE_CHOICES,
        max_length=255, blank=True
    )
    full_name = models.CharField(
        'Full name', max_length=255, blank=True
    )
    activation_code = models.CharField(max_length=36, blank=True)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def str(self):
        return '{name} < {email}'.format(
            name=self.full_name,
            email=self.email
        )

    def create_activation_code(self):
        self.activation_code = str(uuid.uuid4())
