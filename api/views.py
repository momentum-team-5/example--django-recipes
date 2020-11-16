from recipes.models import Recipe
from api.serializers import RecipeSerializer
from rest_framework.generics import ListCreateAPIView


class RecipeListView(ListCreateAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return Recipe.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
