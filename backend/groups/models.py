from django.db import models



class Group(models.Model):
    members = models.ManyToManyField("users.CustomUser", related_name="group_members",)

    title = models.CharField(max_length=256, null=False, blank=False)
    code = models.CharField(null=False, blank=False, max_length=256, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='expense/group/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Kick(models.Model):
    target = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="kick_target")
    owner = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="kick_owner")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="kick_group")

    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    vote_needed = models.IntegerField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class KickVote(models.Model):
    owner = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="kickvote_owner")
    kick = models.ForeignKey(Kick, on_delete=models.CASCADE, related_name="kickvote_kick")

    description = models.TextField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
