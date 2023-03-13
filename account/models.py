from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="users_followers", blank=True)
    followings = models.ManyToManyField(User, related_name="users_followings", blank=True)
    profile_pic = models.ImageField(upload_to="img/")

    def __str__(self):
        return f"{self.user}"


class Images(models.Model):
    images = models.ImageField(upload_to="posts/")
    caption = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.caption}"


class Videos(models.Model):
    videos = models.FileField(upload_to="postvideo/")
    caption = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.caption}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.comment}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    images = models.ManyToManyField(Images, blank=True)
    videos = models.ManyToManyField(Videos, blank=True)
    post_description = models.CharField(max_length=100, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="users_likes", blank=True)
    comments = models.ManyToManyField(Comment, related_name="users_comments", blank=True)
