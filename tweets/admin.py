from django.contrib import admin
from .models import Tweet

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'image', 'date_created']
