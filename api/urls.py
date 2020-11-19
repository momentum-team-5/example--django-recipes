from django.urls import path
from api import views as api_views

urlpatterns = [
    path("recipes/", api_views.RecipeListView.as_view()),
    path("recipes/<int:pk>/", api_views.RecipeDetailView.as_view()),
    path("ingredients/", api_views.IngredientCreateView.as_view()),
    path("ingredients/<int:pk>/", api_views.IngredientDetailView.as_view()),
]
