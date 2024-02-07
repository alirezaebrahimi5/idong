from django.contrib import admin

from .models import Expense, ExpenseVote


class KickVoteInline(admin.TabularInline):
    model = ExpenseVote
    extra = 0


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
