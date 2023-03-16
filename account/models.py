from django.db import models
from django.contrib.auth.models import User


# Create your models here.

def user_directory(instance, filename):
    return f"{0}/{1}".format(instance.user.id, filename)


class Comment(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="comment_like")
    commented_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_username()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile/pic/')
    follow = models.ManyToManyField(User, related_name='user_follow', blank=True)
    bio = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_username()


class Post(models.Model):
    user = models.ForeignKey(User, related_name='post_user', on_delete=models.CASCADE)
    media = models.FileField(upload_to='media/')
    caption = models.CharField(max_length=100, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    comments = models.ManyToManyField(Comment, related_name='post_comment', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_username()
