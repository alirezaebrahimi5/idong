from django.db import models


from users.models import CustomUser as User


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_owner')
    users = models.ManyToManyField(User, related_name='cart_users')
    total_price = models.FloatField(default=0)
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
    price = models.FloatField(default=0)
    count = models.PositiveIntegerField(default=1,)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartVote(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

