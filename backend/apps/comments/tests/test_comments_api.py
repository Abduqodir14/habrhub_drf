from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from apps.posts.models import Post
from apps.comments.models import Comment


COMMENT_URL = reverse('comments:create')


def sample_user(username='owl', password='testpass123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


def sample_post():
    """Create a sample post"""
    defaults = {
        'title': 'Test Post',
        'description': 'quis enim lobortis scelerisque fermentum dui faucibus in ornare',
        'category': 'test'
    }

    return Post.objects.create(author=sample_user(), **defaults)


def sample_comment():
    """Create a sample comment"""
    post = sample_post()

    payload = {
        'post': Post.objects.get(id=post.id),
        'content': 'test comment'
    }

    return Comment.objects.create(author=post.author, **payload)


class PrivatePostApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='owl2',
            password='test123'
        )
        self.client.force_authenticate(self.user)

    def test_create_comment(self):
        """Test creating comment"""
        post = sample_post()

        payload = {
            'post': post.id,
            'content': 'test comment'
        }

        res = self.client.post(COMMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.get(id=res.data['id'])
        self.assertEqual(payload['post'], comment.post.id)
        self.assertEqual(payload['content'], comment.content)

    def test_create_reply_comment(self):
        """Test creating reply for other user in comments"""
        comment = sample_comment()

        payload = {
            'post': comment.post.id,
            'parent': comment.id,
            'content': 'test comment for reply in comments'
        }

        res = self.client.post(COMMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.get(id=res.data['id'])
        self.assertEqual(payload['parent'], comment.parent.id)

