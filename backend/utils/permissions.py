from rest_framework.permissions import BasePermission


class IsOwnerOrIsAdmin(BasePermission):

  def has_permission(self, request, view):
    user = request.user
    user_id = request.data.get("user", None)
    is_admin = user.is_staff
    is_owner = False
    if user_id:
      is_owner = user.id == int(user_id)
    return is_owner or is_admin 