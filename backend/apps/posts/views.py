from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.cache import cache
from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer, PostDetailSerializer, VoteSerializer, PostAnalyticsSerializer
from apps.posts.services import vote_manager, analis_votes
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

    @method_decorator(cache_page(5*60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



class VoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Vote and save or delete your vote"""
        vote_manager(pk, request.user)
        return Response(status=201)


class PostAnalyticsVotes(APIView):

    def get(self, request, pk):
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        serializer = PostAnalyticsSerializer(data={'date_from': date_from, 'date_to': date_to})
        serializer.is_valid(raise_exception=True)
        return Response(analis_votes(pk, date_from, date_to), status=status.HTTP_200_OK)


# class PostAnalyticsViews(APIView):





