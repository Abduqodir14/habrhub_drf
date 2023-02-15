from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer, PostDetailSerializer, VoteSerializer
from apps.posts.services import vote_manager
from core.permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return PostDetailSerializer

        return self.serializer_class


class VoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Vote and save or delete your vote"""
        vote_manager(pk, request.user)
        return Response(status=201)





