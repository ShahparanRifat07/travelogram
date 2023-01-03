from django.db import models
from django.contrib.auth.models import AbstractUser
from .utility import upload_dir_path
import random
from auditlog.registry import auditlog
from axes.models import AccessAttempt,AccessFailureLog,AccessLog


# Create your models here.

class CustomUser(AbstractUser):
    # phone_number = models.CharField(max_length=14)
    pass

    @property
    def full_name(self):
        return self._full_name


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=128, blank=True, null=True)
    about = models.CharField(max_length=256, blank=True)
    followers = models.ManyToManyField(CustomUser, blank=True, related_name='followers')
    profile_pic = models.ImageField(default='img/avatar.png', upload_to=upload_dir_path)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



class Code(models.Model):
    number = models.CharField(max_length=6, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        number_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        code_item = []
        for i in range(6):
            num = random.choice(number_list)
            code_item.append(num)
        code_string = ""
        for i in range(len(code_item)):
            code_string = code_string + str(code_item[i])
        self.number = code_string
        super().save(*args, **kwargs)


class UserRequestIP(models.Model):
    ip_address = models.GenericIPAddressField(null=True)
    user = models.OneToOneField(CustomUser,  on_delete=models.CASCADE)
    path_info = models.CharField(max_length=255)
    attempt_time = models.DateTimeField(auto_now=True)
    attempt_numbers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


auditlog.register(Profile)
auditlog.register(AccessAttempt)
auditlog.register(AccessFailureLog)
auditlog.register(AccessLog)
