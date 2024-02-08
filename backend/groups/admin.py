from django.contrib import admin

from .models import Group, Kick, KickVote


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


class KickVoteInline(admin.TabularInline):
    model = KickVote
    extra = 0


@admin.register(Kick)
class KickAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

    inlines = [KickVoteInline, ]
