from django.urls import path
from .views import (TweetListCreateView, TweetRetrieveDeleteView,
    MyTweetListView, MyNewsFeedListView)

app_name = "tweets"
urlpatterns = [
    path('', TweetListCreateView, name="tweet"),
    path('mytweets', MyTweetListView, name="mytweet"),
    path('mynewsfeed', MyNewsFeedListView, name="mynewsfeed"),
    path('<int:id>', TweetRetrieveDeleteView, name="tweet-detail"),
]
