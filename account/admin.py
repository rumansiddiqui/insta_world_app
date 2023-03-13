from django.contrib import admin

from .models import UserProfile, Post, Image, Video, Comment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'pic')
    search_fields = ('user',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption')
    search_fields = ('user',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'caption')
    search_fields = ('caption', )

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('video', 'title')
    search_fields = ('title', )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text')
    search_fields = ('user', )
