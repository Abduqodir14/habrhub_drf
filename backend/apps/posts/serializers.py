from rest_framework import serializers

from apps.posts.models import Post, Vote
from apps.comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['description'] = instance.description[:300]
        return representation

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'description', 'image', 'thumbnail', 'category', 'author')

        # def get_image(self, obj):
        #     return obj.get_image()
        #
        # def get_thumbnail(self, obj):
        #     return obj.get_thumbnail()


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vote
        fields = '__all__'


class PostAnalyticsSerializer(serializers.Serializer):
    date_from = serializers.DateTimeField(required=True)
    date_to = serializers.DateTimeField(required=True)





