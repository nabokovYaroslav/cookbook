from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter

from recipes.api.viewsets import RecipeViewSet, CategoryRecipeViewSet, CategoryViewSet, ViewViewSet, RecipeCommentViewSet
from users.api.viewsets import UserViewset

router = SimpleRouter()
router.register('recipes', RecipeViewSet, basename="recipes")
router.register('users', UserViewset, basename="users")
router.register('categories', CategoryViewSet, basename="categories")

category_router = NestedSimpleRouter(router, "categories", lookup="category")
category_router.register("recipes", CategoryRecipeViewSet, basename="recipes of categories")

recipe_router = NestedSimpleRouter(router, "recipes", lookup="recipe")
recipe_router.register("comments", RecipeCommentViewSet, basename="comments of recipes")
recipe_router.register("views", ViewViewSet, basename="views of recipes")

urlpatterns = [
    path('authentication/', include('authentication.api.urls')),
    path('', include(router.urls)),
    path('', include(category_router.urls)),
    path('', include(recipe_router.urls))
]
