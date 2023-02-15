from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


# CREATE_USER_URL = reverse('users:users-list')
#
# def detail_url(user_id):
#     """Return users detail url"""
#     return reverse('users:users-detail', args=[user_id])

CREATE_USER_URL = reverse('users:create')
ACCOUNT_URL = reverse('users:account')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating with valid payload is successful"""
        payload = {
            'username': 'owl',
            'email': 'sseeleyyy@gmail.com',
            'password': 'testpass123',
            'first_name': 'Abdukodir',
            'last_name': 'Ortikov',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """Test creating a user that already exists fails"""
        payload = {'username': 'owl', 'password': 'testpass123'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {'username': 'owl', 'password': 'p12'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(username=payload['username']).exists()
        self.assertFalse(user_exists)


class PrivateUserApiTests(TestCase):
    """Test API request that require authentication"""

    def setUp(self):
        payload = {
            'username': 'owl',
            'email': 'sseeleyyy@gmail.com',
            'password': 'testpass123',
            'first_name': 'Abdukodir',
            'last_name': 'Ortikov',
        }
        self.user = create_user(**payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged  in used"""
        res = self.client.get(ACCOUNT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'username': 'owl',
            'email': 'sseeleyyy@gmail.com',
            'first_name': 'Abdukodir',
            'last_name': 'Ortikov',
            'bio': '',
            'skills': ''
        })

    def test_post_me_not_allowed(self):
        """Test that POST not allowed on me url"""
        res = self.client.post(ACCOUNT_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating that user profile for authenticated user"""
        payload = {'username': 'owl14', 'password': 'test12345'}
        res = self.client.patch(ACCOUNT_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, payload['username'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)











