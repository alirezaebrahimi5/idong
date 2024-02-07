from django.db import models

from backend.users.models import CustomUser as User


class Group(models.Model):
    members = models.ManyToManyField(User,)

    title = models.CharField(max_length=256, null=False, blank=False)
    code = models.CharField(null=False, blank=False,)
    image = models.ImageField(null=False, blank=False, upload_to='expense/group/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Expense(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    users = models.ManyToManyField(User, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(null=True, blank=True)
    users_num = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="expense/expense/", null=True, blank=True)
    is_close = models.BooleanField(default=False,)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ExpenseVote(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE,)  # TODO check if need to be onetoone

    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="expense/vote/", null=True, blank=True)
























