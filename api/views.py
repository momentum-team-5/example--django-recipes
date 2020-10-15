from django.core.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from recipes.models import Recipe, Ingredient
from .serializers import IngredientSerializer, RecipeSerializer

# class RecipeListView(APIView):
#     def get(self, request, format=None):
#         recipes = Recipe.objects.for_user(request.user)
#         serializer = RecipeSerializer(recipes, many=True)
#         return Response(serializer.data)

class RecipeListView(ListCreateAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return Recipe.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Recipe.objects.for_user(self.request.user)
        return self.request.user.recipes

class IngredientCreateView(CreateAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def perform_create(self, serializer):
        recipe = serializer.validated_data['recipe']
        if self.request.user != recipe.user:
            raise PermissionDenied()
        serializer.save()

class IngredientDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        return Ingredient.objects.filter(recipe__user=self.request.user)

"""
GET    /api/recipes/      Get a list of all recipes you are allowed to see
POST   /api/recipes/      Create a new recipe
GET    /api/recipes/<id>/ Get one recipe
PUT    /api/recipes/<id>/ Replace a recipe
PATCH  /api/recipes/<id>/ Update a recipe
DELETE /api/recipes/<id>/ Delete a recipe

POST   /api/ingredients/       Add an ingredient to a recipe
PATCH  /api/ingredients/<pk>/  Update an ingredient
PATCH  /api/ingredients/<pk>/  Delete an ingredient
"""
