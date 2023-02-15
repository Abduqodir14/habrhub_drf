from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.posts.models import Post


def sample_user(username='owl', password='testpass123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)

class ModelTests(TestCase):

    def test_post_str(self):
        """Test the post string representation"""
        description = 'quis enim lobortis scelerisque fermentum dui faucibus in ornare'
        post = Post.objects.create(
            author=sample_user(),
            title='Test Post',
            description=description,
            category='test'
        )

        self.assertEqual(str(post), f'{post.author} - {post.title}')

    # def test_post_slug:
    # def test_image_validator
    #def test_thumbnail (we can test its sizes)
    # def test_vote_str: