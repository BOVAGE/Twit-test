from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.urls import reverse
from .models import Tweet
from django.contrib.auth import get_user_model
from .serializers import TweetSerializer
from rest_framework.test import force_authenticate
from .views import TweetListCreateView

User = get_user_model()

class TweetTests(TestCase):

    def setUp(self):
        self.testuser = User.objects.create_user(username="testuser", password="password123")
        self.testtweet = Tweet.objects.create(creator=self.testuser, text="Hello world")

    def test_tweet_content(self):
        tweet = Tweet.objects.get(id=self.testtweet.id)
        user = User.objects.get(id=self.testuser.id)
        expected_object_name = f'{tweet.text}'
        self.assertEqual(expected_object_name, "Hello world")
        self.assertEqual(tweet.creator, user)


class TweetListViewTests(TestCase):
    """
        Test for GET all tweets API
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.testuser = User.objects.create_user(username="testuser", password="password123")
        tweets_to_create = [Tweet(creator=self.testuser, text=f"Hello world{i}") for i in range(5)]
        tweet_objs = Tweet.objects.bulk_create(tweets_to_create)

    def test_get_all_tweets(self):
        request = self.factory.get(reverse('tweets:tweet'))
        view = TweetListCreateView
        force_authenticate(request, user=self.testuser)
        response = view(request)
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True, context={'request': request})
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)