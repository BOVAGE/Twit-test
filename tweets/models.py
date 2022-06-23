from distutils.command.upload import upload
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Tweet(models.Model):
    creator = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    image = models.ImageField(upload_to="post_images/", blank=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.text