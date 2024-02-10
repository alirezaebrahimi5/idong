from rest_framework import serializers

from .models import Cart, Product
from groups.models import Group
from users.models import CustomUser as User, CustomUser


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
        exclude = ("updated_at", )


class ProductUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=True)
    title = serializers.CharField(allow_null=True, allow_blank=True, required=True)
    price = serializers.IntegerField(allow_null=False, required=True)
    count = serializers.IntegerField(allow_null=False, required=True)

    class Meta:
        model = Product
        exclude = ("created_at", "updated_at", "cart")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "pfp")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title", "image", "created_at")


class CartDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        exclude = ("updated_at", )

    def get_owner(self, obj):
        owner = CustomUser.objects.get(id=obj.owner.id)
        return UserSerializer(owner).data

    def get_users(self, obj):
        users = obj.users.all()
        return UserSerializer(users, many=True).data

    def get_group(self, obj):
        group = Group.objects.get(id=obj.group.id)
        return GroupSerializer(group).data
