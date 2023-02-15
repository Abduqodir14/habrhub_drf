from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.followers.models import Follower



def sample_user(username, password):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):

    def setUp(self):
        self.user1 = sample_user('owl1', 'testpass123')
        self.user2 = sample_user('owl2', 'test123')

    def test_follower_str(self):
        """Test the follower string representation"""
        follower = Follower.objects.create(user=self.user1, subscriber=self.user2)

        self.assertEqual(str(follower), f'{follower.subscriber} follows {follower.user}')

