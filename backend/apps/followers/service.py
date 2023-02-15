from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from apps.followers.models import Follower
from apps.followers.serializers import FollowerSerializer


def filter_objects(model, **kwargs):
    return model.objects.filter(**kwargs)


def follow_user(request, pk):
    follower = filter_objects(Follower, user=get_user_model().objects.get(pk=pk), subscriber=request.user)

    if follower.exists():
        raise ValidationError('You have already followed for this user')

    serializer = FollowerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=get_user_model().objects.get(pk=pk), subscriber=request.user)


def unfollow_user(request, pk):
    follower = filter_objects(Follower, user=get_user_model().objects.get(pk=pk), subscriber=request.user)

    if follower.exists():
        return follower.delete()

    raise ValidationError('You did not followed for this user')


