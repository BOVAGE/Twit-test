from atexit import register
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()
SIGNING_KEY = settings.SIMPLE_JWT['SIGNING_KEY']
ALGORITHM = settings.SIMPLE_JWT['ALGORITHM']

class UserModelTests(TestCase):

    def setUp(self):
        self.simple_user = User.objects.create_user(username="testuser", email="test@gmail.com",
        password="123456")

        self.super_user = User.objects.create_superuser(username="superuser", email="supertest@gmail.com",
        password="123456")

    def test_simple_user(self):
        simple_user = User.objects.get(id=self.simple_user.id)
        self.assertEqual(simple_user.is_staff, False)
        self.assertEqual(simple_user.is_active, True)

    def test_super_user(self):
        super_user = User.objects.get(id=self.super_user.id)
        self.assertEqual(super_user.is_staff, True)
        self.assertEqual(super_user.is_active, True)

    def test_user_token(self):
        self.assertIn("refresh", self.simple_user.get_tokens().keys())
        self.assertIn("access", self.simple_user.get_tokens().keys())
        access_token = self.simple_user.get_tokens()['access']
        id_from_token = jwt.decode(access_token, SIGNING_KEY, [ALGORITHM])['user_id']
        self.assertEqual(self.simple_user.id, id_from_token)


class FollowerViewTests(APITestCase):

    def test_no_followers(self):
        register_url = reverse('users:register')
        data = {
            'username': 'testuser',
            'password': 'password',
            'password2': 'password'
        }
        response = self.client.post(register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='testuser')
        url = reverse('users:follower', args=(user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)