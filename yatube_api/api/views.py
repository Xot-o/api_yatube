from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Group
from .serializers import PostSerializer, CommentSerializer, GroupSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Класс доступа, проверяет что автор запроса = автор поста, иначе дает доступ только для чтения.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class PostViewSet(viewsets.ModelViewSet):
    """
    Вью сет постов. Просмотр доступен после аутентификации, изменения поста только автору.
    """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    """
    Вью сет групп. Изменение доступно только через админку.
    """

    permission_classes = [IsAuthenticated]

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вью сет комментариев. Просмотр доступен после аутентификации, изменения комментария только автору.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
