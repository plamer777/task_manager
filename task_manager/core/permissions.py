from rest_framework.permissions import BasePermission
# ----------------------------------------------------------------------------


class UserProfilePermission(BasePermission):
    message = 'Only owner can review, update and delete this profile'

    def has_permission(self, request, view):

        if request.user.pk == view.kwargs.get('pk'):
            return True

        return False
