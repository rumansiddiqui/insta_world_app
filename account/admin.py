from django.contrib import admin

from account.models import Profile, Post, Image, Video, Comment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_pic')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post_description')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'video')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment')
