from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from apps.followers.models import Follower


FOLLOWER_URL = reverse('followers:followers-list')


def detail_url(user_id):
    """Return follower detail url"""
    return reverse('followers:followers-detail', args=[user_id])


def sample_user(username, password):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


def sample_following(user1, user2):
    return Follower.objects.create(user=user1, subscriber=user2)


class PublicPostApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='owl',
            password='testpass123'
        )

    def test_auth_required(self):
        """Test that authentication is required for following"""
        res = self.client.post(FOLLOWER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='owl1',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_follow_user(self):
        """Test following user"""
        user = sample_user('owl123', 'pass12345')

        res = self.client.post(detail_url(user.id))

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        follower = Follower.objects.filter(user=user, subscriber=self.user).exists()

        self.assertTrue(follower)

    def test_unfollow(self):
        """Tets unfollow user"""
        user = sample_user('owl123', 'pass12345')
        sample_following(user, self.user)

        res = self.client.delete(detail_url(user.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)




