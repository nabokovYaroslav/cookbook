from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from users.models import User
from users.api.serializers import UserSerializer, UserBasicSerializer, RegisterUserSerializer
from utils.permissions import IsOwnerOrIsAdmin


class UserViewset(viewsets.ModelViewSet):

    lookup_field = "user_name"

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer
        elif self.action == "retrieve":
            if IsOwnerOrIsAdmin().has_permission(request=self.request, view=self):
                return UserSerializer
            else:
                return UserBasicSerializer
        return UserSerializer  

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