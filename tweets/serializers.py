from rest_framework import serializers
from .models import Tweet
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()
class TweetSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.HyperlinkedRelatedField(read_only=True, view_name='users:profile', lookup_url_kwarg='id')
    url = serializers.HyperlinkedIdentityField(view_name='tweets:tweet-detail', lookup_url_kwarg='id')
    creator_name = serializers.CharField(source='creator.username', read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'url', 'creator', 'creator_name', 'text', 'image', 'date_created']