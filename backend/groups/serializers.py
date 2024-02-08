from rest_framework import serializers

from groups.models import Group
from users.models import CustomUser as User


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "last_login", "pfp")


class GroupAllSerializer(serializers.ModelSerializer):
    members = MembersSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ("id", "members", "title", "image",)


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("title", "image",)


class GroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("title", "image", "id")