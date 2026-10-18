from rest_framework.permissions import BasePermission
from .models import AdminUser


class IsActiveAdmin(BasePermission):
    message = "Active administrator access is required."

    def has_permission(self, request, view):
        user = request.user
        if not getattr(user, "is_authenticated", False):
            return False

        return AdminUser.objects.filter(
            supabase_user_id=user.id,
            is_active=True,
        ).exists()