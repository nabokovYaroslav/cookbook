from django.db.models import Count

from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny

from recipes.api.serializers import (
                                     RecipeListSerializer, RecipeCreateUpdateSerializer, RecipeDestroySerializer, 
                                     RecipeRetrieveSerializer, RecipeWidgetSerializer, RecipeSearchSerializer
                                     )
from utils.permissions import IsOwnerOrIsAdmin
from recipes.models import Recipe


class RecipeViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.action == "list":
            return RecipeListSerializer
        elif self.action == "retrieve":
            return RecipeRetrieveSerializer
        elif self.action == "destroy":
            return RecipeDestroySerializer
        return RecipeCreateUpdateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ("list", "retrieve"):
            context["extension_image"] = self.request.META["extension_image"]
        return context

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            permission_classes = (IsAuthenticated, IsOwnerOrIsAdmin,) 
        elif self.action == "create":
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (AllowAny,)
        return (permission() for permission in permission_classes)
    
    def get_queryset(self):
        if self.action == "list":
            return Recipe.objects.select_related("category").annotate(views_count=Count("view")).annotate(comments_count=Count('comment'))
        elif self.action == "retrieve":
            return Recipe.objects.select_related("category", "user").prefetch_related("ingredients", "steps").annotate(views_count=Count('view')).annotate(comments_count=Count('comment'))
        elif self.action == "destroy":
            return Recipe.objects.all()
        return Recipe.objects.prefetch_related("ingredients", "steps")
    