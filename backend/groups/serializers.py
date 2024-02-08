from rest_framework import serializers

from .models import Group, Kick, KickVote
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


class KickCreateSerializer(serializers.Serializer):
    target = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    group = serializers.IntegerField(required=True, allow_null=False)
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    description = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class KickSerializer(serializers.ModelSerializer):
    vote_needed = serializers.SerializerMethodField()

    class Meta:
        model = Kick
        exclude = ("updated_at", )

    def get_vote_needed(self, obj):
        count = Group.objects.get(id=obj.group.id)
        return count.members.count() - 2


