from rest_framework import serializers

from .models import Cart, Product


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


class CartProductSerializer(serializers.ModelSerializer):
    description = serializers.CharField(allow_null=True, allow_blank=True, default="No description")

    class Meta:
        model = Product
        exclude = ("created_at", "updated_at", )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("created_at", )


class ProductUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=True)
    title = serializers.CharField(allow_null=True, allow_blank=True, required=True)
    price = serializers.IntegerField(allow_null=False, required=True)
    count = serializers.IntegerField(allow_null=False, required=True)

    class Meta:
        model = Product
        exclude = ("created_at", "updated_at", "cart")