from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LoginCode


@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    list_display = ('id', 'email', 'name', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('name',)}),
        # ('Personal Info', {'fields': ('name', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        # ('resturant', {'fields': ('restaurant_rel',)}),
        ('Important dates', {'fields': ('last_login', )}),)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'password1', 'password2', 'is_active', 'is_superuser', 'is_staff'),
        }),
    )
    search_fields = ('name', 'email')


@admin.register(LoginCode)
class LoginCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
