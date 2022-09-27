from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

    @property
    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'