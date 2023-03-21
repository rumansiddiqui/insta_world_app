from django.db import models
from django.contrib.auth.models import User
from post.utils import user_upload_path


class Profile(models.Model):
    """Model for all profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_upload_path)
    follow = models.ManyToManyField(User, related_name='user_follow', blank=True)
    bio = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        """String representation for Profile"""
        return self.user.get_username()

