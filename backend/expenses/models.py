from django.db import models

from users.models import CustomUser as User
from groups.models import Group


class Expense(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="expense_owner")
    users = models.ManyToManyField(User, null=True, blank=True, related_name="expense_users")
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
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
























