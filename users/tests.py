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
# Create your tests here.
class UserModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        simple_user = User.objects.create_user(username="testuser", email="test@gmail.com",
        password="123456")

        super_user = User.objects.create_superuser(username="superuser", email="supertest@gmail.com",
        password="123456")

    def test_simple_user(self):
        simple_user = User.objects.get(id=1)
        self.assertEqual(simple_user.is_staff, False)
        self.assertEqual(simple_user.is_active, True)

    def test_super_user(self):
        super_user = User.objects.get(id=2)
        self.assertEqual(super_user.is_staff, True)
        self.assertEqual(super_user.is_active, True)

    def test_user_token(self):
        simple_user = User.objects.get(id=1)
        self.assertIn("refresh", simple_user.get_tokens().keys())
        self.assertIn("access", simple_user.get_tokens().keys())
        access_token = simple_user.get_tokens()['access']
        id_from_token = jwt.decode(access_token, SIGNING_KEY, [ALGORITHM])['user_id']
        self.assertEqual(simple_user.id, id_from_token)


# class FollowerViewTests(APITestCase):

#     def test_no_followers(self):
#         register_url = reverse('users:register')
#         data = {
#             'username': 'testuser',
#             'password': 'password',
#             'password2': 'password'
#         }
#         response = self.client.post(register_url, data)
#         print(response.status_code)
#         print(response.data)
#         # url = reverse('users:follower', args=(1,))
#         # print(">>>>>",url)
#         # response = self.client.get(url)
#         # self.assertEqual(response.status_code, status.HTTP_200_OK)