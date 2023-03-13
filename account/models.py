from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="img/", null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='following')
    created_on = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.caption}"


class Video(models.Model):
    video = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_comment = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    caption = models.CharField(max_length=100)
    comments = models.ManyToManyField(Comment)
    images = models.ManyToManyField(Image)
    videos = models.ManyToManyField(Video)
    likes = models.ManyToManyField(User, blank=True, related_name="users_likes")
    shares = models.ManyToManyField(User, blank=True, related_name="user_share")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __int__(self):
        return self.user
