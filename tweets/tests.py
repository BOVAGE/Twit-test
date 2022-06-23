from django.test import TestCase
from .models import Tweet
from django.contrib.auth import get_user_model

User = get_user_model()

class TweetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        testuser = User.objects.create_user(username="testuser", password="password123")
        Tweet.objects.create(creator=testuser, text="Hello world")

    def test_tweet_content(self):
        tweet = Tweet.objects.get(id=1)
        user = User.objects.get(id=1)
        expected_object_name = f'{tweet.text}'
        self.assertEqual(expected_object_name, "Hello world")
        self.assertEqual(tweet.creator, user)