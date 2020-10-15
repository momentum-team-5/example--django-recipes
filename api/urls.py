from django.urls import include, path
from rest_framework import routers

from api import views as api_views

api_router = routers.DefaultRouter()
api_router.register('recipes', api_views.RecipeViewSet, basename="recipe")

urlpatterns = [
    path('ingredients/', api_views.IngredientCreateView.as_view(), name="ingredient-list"),
    path('ingredients/<int:pk>/', api_views.IngredientDetailView.as_view(), name="ingredient-detail"),
    path('', include(api_router.urls)),
]
