from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingList,
    Subscribe,
    Tag,
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name", "measurement_unit")
    list_filter = ("name",)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = (
        "author",
        "name",
        "text",
        "tags",
        "image",
        "cooking_time",
        "favorites_count",
    )
    list_display = (
        "name",
        "author",
    )
    search_fields = (
        "name",
        "author",
    )
    list_filter = ("name", "author", "tags")
    readonly_fields = ("favorites_count",)
    inlines = [RecipeIngredientInline]
    autocomplete_fields = ("author",)

    def favorites_count(self, obj):
        return Favorite.objects.filter(favorite=obj).count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "favorite",
    )
    autocomplete_fields = (
        "user",
        "favorite",
    )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    autocomplete_fields = ["ingredient", "recipe"]


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "follower",
    )
    autocomplete_fields = (
        "author",
        "follower",
    )


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "cart",
    )
    autocomplete_fields = (
        "author",
        "cart",
    )
