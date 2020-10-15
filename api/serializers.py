from rest_framework import serializers
from recipes.models import Ingredient, Recipe


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'url',
            'amount',
            'item',
            'recipe'
        ]

class EmbeddedIngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'url',
            'amount',
            'item',
        ]

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField()
    ingredients = EmbeddedIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'url',
            "title",
            "cook_time_in_minutes",
            "prep_time_in_minutes",
            "user",
            "ingredients",
            "public",
        ]


