from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.followers.models import Follower
from apps.followers.serializers import ListFollowerSerializer
from apps.followers.service import filter_objects, follow_user, unfollow_user


class ListFollowerView(generics.ListAPIView):
    serializer_class = ListFollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return filter_objects(Follower, self.request.user)


class FollowerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Following user"""
        follow_user(self.request, pk)
        return Response(status=201)

    def delete(self, request, pk):
        """Unfollowing user"""
        unfollow_user(self.request, pk)
        return Response(status=200)


