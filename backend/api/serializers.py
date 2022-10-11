from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField("get_is_subscribed")

    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )
        model = User

    def get_is_subscribed(self, obj):
        return getattr(obj, "is_subscribed", False)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientRecipeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class IngredientCreateRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField("get_favorited")
    is_in_shopping_cart = serializers.SerializerMethodField(
        "get_shopping_cart"
    )
    ingredients = IngredientRecipeSerializer(
        source="related_ingredients", many=True
    )
    cooking_time = serializers.IntegerField(min_value=0)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "pub_date",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "cooking_time",
            "text",
        )

    def get_favorited(self, obj):
        return getattr(obj, "is_favorited", False)

    def get_shopping_cart(self, obj):
        return getattr(obj, "is_in_shopping_cart", False)


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientRecipeSerializer(
        many=True, source="related_ingredients"
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    @staticmethod
    def parse_ingredients(recipe, data):
        for ingredient_data in data:
            try:
                ingredient_current = Ingredient.objects.get(
                    pk=ingredient_data["ingredient"]["id"]
                )
            except serializers.ValidationError:
                raise serializers.ValidationError("Miss ingredient")
            IngredientRecipe.objects.create(
                recipe=recipe,
                amount=ingredient_data["amount"],
                ingredient=ingredient_current,
            )

    def create(self, validated_data):
        if "tags" in validated_data:
            tags = validated_data.pop("tags")
        ingredients_data = validated_data.pop("related_ingredients")
        recipe = super().create(validated_data)
        recipe.tags.add(*tags)
        self.parse_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        if "tags" in validated_data:
            tags = validated_data.pop("tags")
            instance.tags.clear()
            instance.tags.add(*tags)
        ingredients_data = validated_data.pop("related_ingredients")
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.parse_ingredients(instance, ingredients_data)
        super().update(instance, validated_data)
        return instance

    def validate(self, data):
        ingredients = []
        for ingredient in data['related_ingredients']:
            if ingredient['ingredient']['id'] not in ingredients:
                ingredients.append(ingredient['ingredient']['id'])
            else:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться!'
                )
        tags = []
        for tag in data["tags"]:
            if tag not in tags:
                tags.append(tag)
            else:
                raise serializers.ValidationError(
                    "Тэги не должны повторяться!"
                )
        return data


class SubscriptionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField("get_is_subscribed")
    recipes = RecipeReadSerializer(many=True)

    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
        )
        model = User

    def get_is_subscribed(self, obj):
        return getattr(obj, "is_subscribe", False)
