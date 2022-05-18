from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from users.models import User
from users.api.serializers import UserSerializer, UserBasicSerializer, RegisterUserSerializer
from utils.permissions import IsOwnerOrIsAdmin


class UserViewset(viewsets.ModelViewSet):

    lookup_field = "user_name"

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer
        elif self.action == "retrieve":
            obj = self.get_object()
            if IsOwnerOrIsAdmin().has_object_permission(request=self.request, view=self, obj=obj):
                return UserSerializer
            else:
                return UserBasicSerializer
        return UserSerializer 

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ("list", "retrieve"):
            context["extension_image"] = self.request.META["extension_image"]
        return context 

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (IsAdminUser,)
        elif self.action in ('destroy', 'update', 'partial_update',):
            permission_classes = (IsOwnerOrIsAdmin,)
        else:
            permission_classes = (AllowAny,)
        return (permission() for permission in permission_classes)

    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=("post",))
    def logout(self, request):
        response = Response(status=HTTP_200_OK)
        response.delete_cookie("refresh")
        return response
