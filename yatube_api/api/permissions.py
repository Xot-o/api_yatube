from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Класс доступа, проверяет что автор запроса = автор поста,
    иначе дает доступ только для чтения.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
