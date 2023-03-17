from django.db import models
from django.contrib.auth.models import User
from account.utils import user_upload_path


class Comment(models.Model):
    """Model for all comment"""
    text = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="comment_like")
    commented_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        """String representation for Comment"""
        return self.user.get_username()


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


class Post(models.Model):
    """Model for all Profile"""
    user = models.ForeignKey(User, related_name='post_user', on_delete=models.CASCADE)
    media = models.FileField(upload_to=user_upload_path)
    caption = models.CharField(max_length=100, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    comments = models.ManyToManyField(Comment, related_name='post_comment', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        """String representation for Post"""
        return self.user.get_username()
