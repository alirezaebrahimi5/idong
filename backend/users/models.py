import random
import string

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager
from groups.models import Group


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True, )
    name = models.CharField(max_length=256, null=True, blank=True)
    pfp = models.ImageField(upload_to="users/profile_pics", null=True, blank=True)

    is_staff = models.BooleanField(default=False, )
    is_superuser = models.BooleanField(default=False, )
    is_active = models.BooleanField(default=False, )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}-{self.name}"

    @property
    def user_is_active(self):
        return self.is_active

    @property
    def user_is_superuser(self):
        return self.is_superuser

    @property
    def get_email(self):
        return self.email


# # used for signup of users
# class SignUpCode(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     code = models.CharField(max_length=10, unique=True)
#
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     @staticmethod
#     def create_token(user: CustomUser):
#         while True:
#             random_code = ''.join(
#                 random.choices(string.digits + string.ascii_letters + string.punctuation) for _ in range(10))
#             code, created = SignUpCode.objects.get_or_create(code=random_code, user=user)
#             if not created:
#                 continue
#             break
#         return code


# used for login the user
class LoginCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    usage_count = models.IntegerField(default=0, null=True, blank=True)

    create_count = models.IntegerField(default=0, null=True, blank=True)
    wait_until = models.DateTimeField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_token(user: CustomUser):
        codes = LoginCode.objects.values_list('code', flat=True)
        while True:
            # create a random string
            random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            if random_code not in codes:
                break
        try:
            LoginCode.objects.create(user=user, code=random_code)
        except:
            # when there is a
            login_code = LoginCode.objects.get(user=user)
            login_code.delete()
            LoginCode.objects.create(user=user, code=random_code)
        return random_code


