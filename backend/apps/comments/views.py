from rest_framework import generics, permissions
from apps.comments.serializers import CommentSerializer


class CreateCommentstView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
