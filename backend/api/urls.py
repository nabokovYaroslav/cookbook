from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter

from recipes.api.viewsets import RecipeViewSet
from users.api.viewsets import UserViewset

router = SimpleRouter()
router.register('recipes', RecipeViewSet, basename="recipes")
router.register('users', UserViewset, basename="users")

urlpatterns = [
    path('authentication/', include('authentication.api.urls')),
    path('', include(router.urls)),
]
