from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Follow, Ingredient, Recipe, RecipeIngredient, Tag
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(user=user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipesListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = RecipeIngredientSerializer(
        many=True, required=True, source='recipe'
    )
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class AmountIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )


class RecipesCreateSerializer(serializers.ModelSerializer):
    ingredients = AmountIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def create_amount_ingredients(self, ingredients, recipe):
        new_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
            for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(new_ingredients)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_amount_ingredients(ingredients, recipe)
        return recipe

    def update(self, obj, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            obj.ingredients.clear()
            self.create_amount_ingredients(ingredients, obj)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            obj.tags.set(tags)
        return super().update(obj, validated_data)

    def to_representation(self, instance):
        serializer = RecipesListSerializer(instance)
        return serializer.data


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(user=obj.user, author=obj.author).exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author).order_by(
            '-pub_date'
        )
        return FavoriteRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
