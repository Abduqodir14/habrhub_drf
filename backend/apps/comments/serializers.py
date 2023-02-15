from rest_framework import serializers

from apps.comments.models import Comment


class FilterReplyListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'parent', 'content')


class CommentsSerializer(serializers.ModelSerializer):
    replies = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        list_serializer_class = FilterReplyListSerializer
        model = Comment
        fields = ('id', 'author', 'content', 'created_at', 'replies')
