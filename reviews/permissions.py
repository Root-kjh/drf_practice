from rest_framework import permissions

class ReviewAuthorOrReadOnly(permissions.BasePermission):
    """
    인증 시 사용자는 자신의 리뷰만 수정할 수 있습니다.
    인증되지 않은 사용자는 읽기 전용입니다.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user