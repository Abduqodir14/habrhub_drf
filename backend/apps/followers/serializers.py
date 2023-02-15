from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.followers.models import Follower


class UserByFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')


class ListFollowerSerializer(serializers.ModelSerializer):
    subscriber = UserByFollowerSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ('subscriber',)


class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = ('id',)
