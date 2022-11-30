from django.db import models
from django.contrib.auth.models import AbstractUser
from .utility import upload_dir_path


# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=14)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    about = models.CharField(max_length=256, blank=True)
    followers = models.ManyToManyField(CustomUser, blank=True, related_name='followers')
    profile_pic = models.ImageField(default='profile.png', upload_to=upload_dir_path)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
