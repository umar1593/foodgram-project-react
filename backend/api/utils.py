from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.serializers import FavoriteRecipeSerializer
from recipes.models import Recipe


class CreateDeleteMixin:
    def add_delete_recipe_to(self, request, model, pk=None):
        recipe_pk = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        if request.method == 'POST':
            serializer = FavoriteRecipeSerializer(recipe)
            model.objects.create(user=self.request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if model.objects.filter(
                user=self.request.user, recipe=recipe
            ).exists():
                model.objects.get(
                    user=self.request.user, recipe=recipe
                ).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепт отсутсвует в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST,
            )
