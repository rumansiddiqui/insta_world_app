from django.contrib import admin

from account.models import Profile, Post, Images, Videos, Comment


@admin.register(Profile)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_pic')


@admin.register(Post)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_description')


@admin.register(Images)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption')


@admin.register(Videos)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption')


@admin.register(Comment)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment')
