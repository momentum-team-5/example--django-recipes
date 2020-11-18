from recipes.models import Recipe
from api.serializers import RecipeSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


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
