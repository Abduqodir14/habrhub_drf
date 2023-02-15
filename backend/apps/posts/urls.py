from django.urls import path, include
from rest_framework import routers

from apps.posts.views import (
    PostViewSet,
    VoteView
)

app_name = 'posts'


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<uuid:pk>/votes/', VoteView.as_view(), name='votes')
]
