from rest_framework import serializers
from recipes.models import Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            "id",
            "amount",
            "item",
        ]


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    tags = serializers.SlugRelatedField(
        many=True, slug_field="tag", queryset=Tag.objects.all()
    )
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "cook_time_in_minutes",
            "prep_time_in_minutes",
            "user",
            "tags",
            "ingredients",
        ]
