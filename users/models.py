from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# models for user's account
class User(AbstractUser):
    bio = models.CharField(max_length=200, blank=True)
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')
    # symmetrical set to false defines non-symmetrical relationship
    # meaning If i follow you, it doesn't imply you automatically following back  
    avatar = models.ImageField(upload_to='avatar_images/', blank=True)
    dob = models.DateField(verbose_name='Date of Birth', blank=True, null=True)

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
