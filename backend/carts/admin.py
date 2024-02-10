from django.contrib import admin

from .models import Cart, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "title")
    inlines = [ProductInline]
