from rest_framework.permissions import BasePermission


class IsOwnerOrIsAdmin(BasePermission):

  def has_permission(self, request, view):
    return request.user.is_staff or request.user.id

  def has_object_permission(self, request, view, obj):
      user = request.user
      is_admin = user.is_staff
      is_user_instance = False
      if hasattr(obj, "is_staff"):
        is_user_instance = True
      if is_user_instance:
        return user.id == obj.id or is_admin
      return user.id == obj.user_id or is_admin