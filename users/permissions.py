from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsTutor(permissions.BasePermission):
    """
    Allows access only to tutor users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'is_tutor', False))


class IsStudent(BasePermission):
    """
    Allows access only to student users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_student)


class IsAdmin(BasePermission):
    """Allows access only to application admin users (is_admin flag)."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'is_admin', False))


class IsAdminOrTutor(BasePermission):
    """Allows access to admins or tutors for management endpoints."""
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (getattr(user, 'is_admin', False) or getattr(user, 'is_tutor', False)))


# Backwards-compatible alias
class IsAdminOrInstructor(IsAdminOrTutor):
    """Compatibility alias for older code using IsAdminOrInstructor."""
    pass


class IsOwnerOrAdminModerator(BasePermission):
    """
    - Tutor can edit/delete ONLY their own course
    - Admin & Moderator can delete any course
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_authenticated:
            return False

        # Admins & moderators can delete any course
        if user.is_admin or user.is_moderator:
            return True

        # Tutor can only modify their own course
        return user.is_tutor and obj.tutor == user
    

# -------------------------------------
# IS ENROLLED STUDENT
# -------------------------------------
# permissions.py
class IsEnrolledStudent(BasePermission):
    """
    Allows access only if the student is enrolled in the course
    related to the object.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated or not user.is_student:
            return False

        from .models import Enrollment, Lesson

        if isinstance(obj, Lesson):
            return Enrollment.objects.filter(
                student=user,
                course=obj.course
            ).exists()

        return False



def check_object_permissions(request, obj, permissions):
    """
    Manually run object-level permissions for function-based views.
    """
    for permission in permissions:
        if not permission.has_object_permission(request, None, obj):
            raise PermissionDenied()
