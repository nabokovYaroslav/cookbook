import re
from random import randint
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models.functions import Lower

from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from recipes.api.serializers import (
                                     RecipeListSerializer, RecipeUpdateSerializer, RecipeDestroySerializer, 
                                     RecipeRetrieveSerializer, RecipeCreateSerialzer, RecipeWidgetSerializer, 
                                     RecipeSearchSerializer, RecipeWidgetSearchSerializer, CategoryListSerializer,
                                     ViewSerializer, CommentCreateDestroySerializer, CommentListSerializer,
                                     RecipeRandomSerializer, CategoryRetrieveSerializer, UnitSerializer,
                                     RecipeEditSerializer,
                                     )
from utils.permissions import IsOwnerOrIsAdmin
from recipes.models import Recipe, Category, Comment, Unit

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
        if re.search("_widget$", self.action):
            self.pagination_class = WidgetResultsSetPagination
        else:
            self.pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action in ("list", "recipes_of_week", "new_recipes", "popular_recipes"):
            return RecipeListSerializer
        elif self.action in ("recipes_of_week_widget", "popular_recipes_widget"):
            return RecipeWidgetSerializer
        elif self.action == "edit":
            return RecipeEditSerializer
        elif self.action == "random_recipes":
            return RecipeRandomSerializer
        elif self.action == "search_widget":
            return RecipeWidgetSearchSerializer
        elif self.action == "search":
            return RecipeSearchSerializer
        elif self.action == "retrieve":
            return RecipeRetrieveSerializer
        elif self.action == "destroy":
            return RecipeDestroySerializer
        elif self.action in ("update", "partial_update"):
            return RecipeUpdateSerializer
        return RecipeCreateSerialzer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["extension_image"] = self.request.META["extension_image"]
        return context

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy", "create", "edit"):
            permission_classes = (IsAuthenticated, IsOwnerOrIsAdmin,) 
        else:
            permission_classes = (AllowAny,)
        return (permission() for permission in permission_classes)
    
    def get_queryset(self):
        if self.action == "list":
            return Recipe.objects.select_related("category").annotate(views_count=Count("views")).annotate(comments_count=Count('comment'))
        elif self.action == "retrieve":
            return Recipe.objects.select_related("category", "user").prefetch_related("ingredients", "steps").annotate(views_count=Count('views')).annotate(comments_count=Count('comment'))
        elif self.action == "destroy":
            return Recipe.objects.all()
        return Recipe.objects.prefetch_related("ingredients", "steps")

    @action(detail=False, methods=("get",))
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

    @action(detail=False, methods=("get",))
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

    @action(detail=False, methods=("get",))
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

    @action(detail=False, methods=("get",))
    def recipes_of_week_widget(self, request):
        queryset = (
                    Recipe
                    .objects
                    .select_related("category")
                    .annotate(views_count=Count("views", filter=Q(views__datetime__range=(timezone.now(), timezone.now() - timedelta(days=7)))))
                    .order_by("-views_count")
                    )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=("get",))
    def popular_recipes_widget(self, request):
        queryset = (
                    Recipe
                    .objects
                    .select_related("category")
                    .annotate(views_count=Count("views"))
                    .order_by("-views_count")
                    )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=("get",))
    def search_widget(self, request):
        queryset = (
                    Recipe
                    .objects
                    .select_related("category")
                    )
        name = request.query_params.get("name")
        if name is not None:
            queryset = queryset.annotate(name_lower=Lower('name')).filter(name_lower__startswith=name.lower())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=("get",))
    def search(self, request):
        queryset = (
                    Recipe
                    .objects
                    .select_related("category")
                    .annotate(views_count=Count("views"))
                    .annotate(comments_count=Count('comment'))
                    )
        name = request.query_params.get("name")
        if name is not None:
            queryset = queryset.annotate(name_lower=Lower('name')).filter(name_lower__startswith=name.lower())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=("get",))
    def random_recipes(self, request):
        count = 6
        recipes_count = Recipe.objects.count()
        queryset = (
                    Recipe
                    .objects
                    .select_related("category")
                    )
        if recipes_count > count:
            end = randint(count, recipes_count)
            start = end - 6
            queryset = queryset[start:end]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=("get",))
    def edit(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
        
class CategoryViewSet(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        else:
            return CategoryRetrieveSerializer
    queryset = Category.objects.all()


class CategoryRecipeViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = RecipeListSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["extension_image"] = self.request.META["extension_image"]
        return context
    
    def get_queryset(self):
        category_pk = self.kwargs.get("category_pk", None)
        base_queryset = Recipe.objects.filter(category_id=category_pk)
        return base_queryset.select_related("category").annotate(views_count=Count("views")).annotate(comments_count=Count('comment'))

class UserRecipeViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = RecipeListSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["extension_image"] = self.request.META["extension_image"]
        return context

    def get_queryset(self):
        user_name = self.kwargs.get("user_user_name", None)
        base_queryset = Recipe.objects.filter(user__user_name=user_name)
        return base_queryset.select_related("category", "user").annotate(views_count=Count("views")).annotate(comments_count=Count('comment'))

class ViewViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = ViewSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrIsAdmin)

class RecipeCommentViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        recipe_pk = self.kwargs.get("recipe_pk", None)
        base_queryset = Comment.objects.filter(recipe_id=recipe_pk)
        return base_queryset.select_related("user")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "list":
            context["extension_image"] = self.request.META["extension_image"]
        return context

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer
        return CommentCreateDestroySerializer
    
    def get_permissions(self):
        if self.action in ("create", "destroy"):
            permission_classes = (IsAuthenticated, IsOwnerOrIsAdmin,) 
        else:
            permission_classes = (AllowAny,)
        return (permission() for permission in permission_classes)

class UnitViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()