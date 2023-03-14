from django.db import models
from django.contrib.auth.models import User


# Create your models here.

def user_directory(instance, filename):
    return f"{0}/{1}".format(instance.user.id, filename)


class Comment(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)
    commented_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Post(models.Model):
    user = models.ForeignKey(User, related_name='post_user', on_delete=models.CASCADE)
    media = models.FileField(upload_to='media/')
    caption = models.CharField(max_length=100, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    comments = models.ManyToManyField(Comment, related_name='post_comment', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"{self.user} Posted this"



# class Like(models.Model):
#     user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE)
#     is_like = models.BooleanField(default=True)
#     liked_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)


# class Follow(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     follower = models.ForeignKey(User, on_delete=models.CASCADE)
#     is_follow = models.BooleanField(default=True)
#     followed_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)



