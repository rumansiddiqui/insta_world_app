from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="users_followers", blank=True)
    followings = models.ManyToManyField(User, related_name="users_followings", blank=True)
    post = models.ManyToManyField(User, related_name="posts", blank=True)
    profile_pic = models.ImageField(upload_to="img/")
    bio = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user}"


class Image(models.Model):
    image = models.ImageField(upload_to="posts/")
    caption = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.caption}"


class Video(models.Model):
    video = models.FileField(upload_to="postvideo/")
    caption = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.caption}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.comment}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image, blank=True)
    videos = models.ManyToManyField(Video, blank=True)
    post_description = models.CharField(max_length=100, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="users_likes", blank=True)
    comments = models.ManyToManyField(Comment, related_name="users_comments", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_posts', blank=True)
