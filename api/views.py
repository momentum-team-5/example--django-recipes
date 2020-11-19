from recipes.models import Ingredient, Recipe
from api.serializers import IngredientWithRecipeSerializer, RecipeSerializer, IngredientSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class RecipeListView(ListCreateAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return Recipe.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # if the request method is GET, the queryset is all viewable recipes
        # otherwise, the queryset is all recipes the current user owns
        if self.request.method == "GET":
            return Recipe.objects.for_user(self.request.user)

        return self.request.user.recipes.all()


class IngredientCreateView(CreateAPIView):
    serializer_class = IngredientWithRecipeSerializer
    queryset = Ingredient.objects.all()

    def perform_create(self, serializer):
        """
        If the recipe we're trying to add an ingredient to doesn't belong
        to the currently logged in user, then raise a 403 Forbidden error.
        """

        recipe = serializer.validated_data['recipe']
        if recipe.user != self.request.user:
            raise PermissionDenied(
                detail="This recipe does not belong to this user.")
        serializer.save()


class IngredientDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        We filter down the ingredients to ones only part of recipes
        owned by the currently logged in user. This prevents other
        users from updating or deleting ingredients from recipes
        they do not own.
        """
        return Ingredient.objects.filter(recipe__user=self.request.user)
