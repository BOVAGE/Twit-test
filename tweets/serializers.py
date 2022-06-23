from rest_framework import serializers
from .models import Tweet
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()
class TweetSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    url = serializers.HyperlinkedIdentityField(view_name='tweets:tweet-detail', lookup_url_kwarg='id')
    creator_profile = serializers.HyperlinkedIdentityField(view_name='users:profile', lookup_url_kwarg='id')
    class Meta:
        model = Tweet
        fields = ['id', 'url', 'creator', 'creator_profile', 'text', 'image', 'date_created']