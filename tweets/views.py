from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from .permissions import IsOwnerOrReadOnly
from .serializers import TweetSerializer
from .models import Tweet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.conf import settings

CACHE_TTL = settings.CACHE_TTL

class ApiRootView(APIView):

    def get(self, request):
        return Response({"twit-fleet": "tweeter-fleet"})

class TweetListCreateView(generics.ListCreateAPIView):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all().select_related('creator')
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [FormParser, MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TweetRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = TweetSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Tweet.objects.all()
    lookup_field = 'id'


class MyTweetListView(generics.ListAPIView):
    """ 
        list tweets created by the authenticated user
    """
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_tweet = self.request.user.tweets.select_related('creator')
        return user_tweet


class MyNewsFeedListView(generics.ListAPIView):
    """ 
        list tweets created by users the authenticated user follows
    """
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        following_ids = self.request.user.following.values_list('id', flat=True)
        return Tweet.objects.filter(creator_id__in=following_ids).select_related('creator')
    
    @method_decorator(cache_page(CACHE_TTL))
    @method_decorator(vary_on_headers("Authorization",))
    # cache requested url for each user
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

ApiRootView = ApiRootView.as_view() 
TweetListCreateView = TweetListCreateView.as_view()
TweetRetrieveDeleteView = TweetRetrieveDeleteView.as_view()
MyTweetListView = MyTweetListView.as_view()
MyNewsFeedListView = MyNewsFeedListView.as_view() 
