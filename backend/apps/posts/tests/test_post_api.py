from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from apps.posts.models import Post, Vote
from apps.posts.serializers import PostSerializer, PostDetailSerializer


POSTS_URL = reverse('posts:posts-list')


def vote_post(post_id):
    """Return vote detail url"""
    return reverse('posts:votes', args=[post_id])


def detail_url(post_id):
    """Return posts detail url"""
    return reverse('posts:posts-detail', args=[post_id])


def sample_user(username='sample', password='testpass123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


def sample_post(author, **params):
    """Create and return post"""
    defaults = {
        'title': 'Sample Post',
        'description': 'quis enim lobortis scelerisque fermentum dui faucibus in ornare',
        'category': 'test'
    }
    defaults.update(params)

    return Post.objects.create(author=author, **defaults)


class PublicPostApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='owl',
            password='testpass123'
        )

    def test_get_posts(self):
        """Test retrieving a list of posts"""
        sample_post(author=self.user)
        sample_post(author=self.user)

        res = self.client.get(POSTS_URL)

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_detail_post(self):
        """Test viewing a post detail"""
        post = sample_post(author=self.user)

        url = detail_url(post.id)
        res = self.client.get(url)

        serializer = PostDetailSerializer(post)
        self.assertEqual(res.data, serializer.data)

    def test_auth_required(self):
        """Test that authentication is required for post Post"""
        defaults = {
            'title': 'Test Post',
            'description': 'quis enim lobortis scelerisque fermentum dui faucibus in ornare',
            'category': 'test'
        }
        res = self.client.post(POSTS_URL, defaults)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='owl',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_create_basic_post(self):
        """Test creating post"""
        payload = {
            'title': 'Test Post',
            'description': 'quis enim lobortis scelerisque fermentum dui faucibus in ornare',
            'category': 'test'
        }

        res = self.client.post(POSTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(post, key))

    def test_partial_update_post(self):
        """Test updating a post with patch"""
        post = sample_post(author=self.user)

        payload = {'title': 'Patch Test Post'}
        url = detail_url(post.id)
        self.client.patch(url, payload)

        post.refresh_from_db()
        self.assertEqual(post.title, payload['title'])

    def test_full_update_post(self):
        """Test updating a post with put"""
        post = sample_post(author=self.user)
        payload = {
            'title': 'Put Test Post',
            'description': 'quis enim lobortis scelerisque fermentum dui faucibus in ornare',
            'category': 'put'
        }
        url = detail_url(post.id)
        self.client.put(url, payload)

        post.refresh_from_db()
        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.description, payload['description'])
        self.assertEqual(post.category, payload['category'])

    def test_create_vote(self):
        """Test upvote for the post"""
        post = sample_post(author=sample_user())

        url = vote_post(post.id)
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)















