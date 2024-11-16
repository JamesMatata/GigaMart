from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    county = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.email
