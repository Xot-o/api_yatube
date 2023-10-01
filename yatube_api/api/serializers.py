from rest_framework import serializers
from posts.models import Post, Comment, Group


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор модели Post. Содержит особую обработку для поля author.
    """
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment. Содержит особую обработку для поля author.
    """
    author = serializers.SlugRelatedField(
        'username', read_only=True
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Group.
    """

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
