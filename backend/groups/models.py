from django.db import models

from users.models import CustomUser as User


class Group(models.Model):
    members = models.ManyToManyField(User,)

    title = models.CharField(max_length=256, null=False, blank=False)
    code = models.CharField(null=False, blank=False, max_length=256, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='expense/group/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

