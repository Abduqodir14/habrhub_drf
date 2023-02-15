from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.comments.models import Comment
from apps.posts.models import Post


def sample_user(username, password):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


def sample_post():
    """Create a sample post"""
    defaults = {
        'title': 'Test Post',
        'description': 'quis enim lobortis scelerisque fermentum dui faucibus in ornare',
        'category': 'test'
    }

    return Post.objects.create(author=sample_user('owl1', 'testpass123'), **defaults)


class ModelTests(TestCase):

    def test_comment_str(self):
        """Test the comment string representation"""
        comment = Comment.objects.create(
            author=sample_user('owl2', 'test123'),
            post=sample_post(),
            content='test comment'
        )

        self.assertEqual(str(comment), f'{comment.author} - {comment.post}')
