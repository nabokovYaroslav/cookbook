from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q

from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from recipes.api.serializers import (
                                     RecipeListSerializer, RecipeUpdateSerializer, RecipeDestroySerializer, 
                                     RecipeRetrieveSerializer, RecipeCreateSerialzer, RecipeWidgetSerializer, RecipeSearchSerializer
                                     )
from utils.permissions import IsOwnerOrIsAdmin
from recipes.models import Recipe

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000

class WidgetResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000


class RecipeViewSet(ModelViewSet):
    def initialize_request(self, request, *args, **kwargs):
        res = super().initialize_request(request, *args, **kwargs)
        self.get_pagination_class()
        return res

    def get_pagination_class(self):
        if self.action in ("recipes_of_week", "new_recipes", "popular_recipes"):
            self.pagination_class = WidgetResultsSetPagination
        else:
            self.pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action in ("list", "recipes_of_week", "new_recipes", "popular_recipes"):
            return RecipeListSerializer
        elif self.action == "retrieve":
            return RecipeRetrieveSerializer
        elif self.action == "destroy":
            return RecipeDestroySerializer
        elif self.action in ("update", "partial_update"):
            return RecipeUpdateSerializer
        return RecipeCreateSerialzer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ("list", "retrieve", "recipes_of_week", "new_recipes", "popular_recipes"):
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
            return Recipe.objects.select_related("category").annotate(views_count=Count("views")).annotate(comments_count=Count('comment'))
        elif self.action == "retrieve":
            return Recipe.objects.select_related("category", "user").prefetch_related("ingredients", "steps").annotate(views_count=Count('view')).annotate(comments_count=Count('comment'))
        elif self.action == "destroy":
            return Recipe.objects.all()
        return Recipe.objects.prefetch_related("ingredients", "steps")

    @action(detail=False, methods=("get",), serializer_class=RecipeListSerializer)
    def recipes_of_week(self, request):
        queryset = (
                    Recipe
                    .objects
                    .select_related("category")
                    .annotate(views_count=Count("views", filter=Q(views__datetime__range=(timezone.now(), timezone.now() - timedelta(days=7)))))
                    .annotate(comments_count=Count('comment'))
                    .order_by("-views_count")
                    )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=("get",), serializer_class=RecipeListSerializer)
    def popular_recipes(self, request):
        queryset = (
                    Recipe
                    .objects
                    .select_related("category")
                    .annotate(views_count=Count("views"))
                    .annotate(comments_count=Count('comment'))
                    .order_by("-views_count")
                    )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=("get",), serializer_class=RecipeListSerializer)
    def new_recipes(self, request):
        queryset = (
                    Recipe
                    .objects
                    .select_related("category")
                    .annotate(views_count=Count("views"))
                    .annotate(comments_count=Count('comment'))
                    .order_by("-id")
                    )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


        