from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from users.models import User
from recipes.models import Subscriber
from users.api.serializers import UserSerializer, UserBasicSerializer, RegisterUserSerializer
from utils.permissions import IsOwnerOrIsAdmin


class UserViewset(viewsets.ModelViewSet):

    lookup_field = "user_name"
    is_owner_or_is_admin = False

    def get_object(self):
        obj = super().get_object()
        if IsOwnerOrIsAdmin().has_object_permission(request=self.request, view=self, obj=obj):
            self.is_owner_or_is_admin = True
        return obj

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer
        elif self.action == "retrieve":
            if self.is_owner_or_is_admin:
                return UserSerializer
            else:
                return UserBasicSerializer
        return UserSerializer 

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["extension_image"] = self.request.META["extension_image"]
        return context 

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (IsAdminUser,)
        elif self.action in ('destroy', 'update', 'partial_update', 'subscribe', 'unsubscribe'):
            permission_classes = (IsAuthenticated, IsOwnerOrIsAdmin,)
        else:
            permission_classes = (AllowAny,)
        return (permission() for permission in permission_classes)

    def get_queryset(self):
        return User.objects.select_related("subscriber")

    @action(detail=False, methods=("post",))
    def logout(self, request):
        response = Response(status=HTTP_200_OK)
        response.delete_cookie("refresh")
        return response
    
    @action(detail=True, methods=("post",),)
    def subscribe(self, request, user_name=None):
        subscriber, created = Subscriber.objects.get_or_create(user=request.user)
        if created:
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Вы уже подписаны"}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=("post",),)
    def unsubscribe(self, request, user_name=None):
        subscriber = get_object_or_404(Subscriber.objects, user=request.user)
        subscriber.delete()
        return Response(status=HTTP_204_NO_CONTENT)