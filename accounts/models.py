from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_technical = models.BooleanField(default=False)
    is_commercial = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class TechnicalUser(CustomUser):
    def save(self, *args, **kwargs):
        self.is_technical = True
        self.is_commercial = False
        if not self.email.endswith('@ngtelecom.noc'):
            raise ValueError('Email must belong to @ngtelecom.noc domain.')
        super().save(*args, **kwargs)

class CommercialUser(CustomUser):
    def save(self, *args, **kwargs):
        self.is_technical = False
        self.is_commercial = True
        if not self.email.endswith('@ngtelecom.sales'):
            raise ValueError('Email must belong to @ngtelecom.sales domain.')
        super().save(*args, **kwargs)

