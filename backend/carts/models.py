from django.db import models

from backend.users.models import CustomUser


class Cart(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    users = models.ManyToManyField(CustomUser,)
    total_price = models.DecimalField()
    users_sum = models.PositiveIntegerField()
    is_confirmed = models.BooleanField(default=False)

    title = models.CharField(max_length=256)
    image = models.ImageField(null=True, blank=True, upload_to="carts/cart")
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField()
    count = models.PositiveIntegerField(default=1,)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartVote(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

