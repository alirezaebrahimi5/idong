from rest_framework import serializers

from .models import Cart


class CartCreateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(allow_null=True, allow_blank=True, default="No description")
    image = serializers.ImageField(allow_null=True, default=None)

    class Meta:
        model = Cart
        exclude = ("created_at", "updated_at", "owner", "is_confirmed", "users_sum", "total_price")


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ("updated_at", )
