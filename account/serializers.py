from django.contrib.auth.models import User
from rest_framework import serializers
import re

from .models import Post, Image, Video, Comment
from .messages import *
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=20, required=True, allow_blank=False, trim_whitespace=True,
                                       error_messages=SIGNUP_VALIDATION_ERROR['first_name'])
    last_name = serializers.CharField(max_length=20, required=False, allow_blank=False, trim_whitespace=True,
                                      error_messages=SIGNUP_VALIDATION_ERROR['last_name'])
    username = serializers.CharField(min_length=4, max_length=20, required=True, allow_blank=False,
                                     error_messages=SIGNUP_VALIDATION_ERROR['username'])
    email = serializers.EmailField(max_length=50, required=True, allow_blank=False,
                                   error_messages=SIGNUP_VALIDATION_ERROR['email'])
    password = serializers.CharField(write_only=True, min_length=8, allow_blank=False,
                                     error_messages=SIGNUP_VALIDATION_ERROR['password'])
    confirm_password = serializers.CharField(write_only=True, min_length=8, allow_null=False,
                                             error_messages=SIGNUP_VALIDATION_ERROR['confirm_password'])

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['password']['not-match'])
        return attrs

    def validate_first_name(self, value):
        if not all(char.isalpha() for char in value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['first_name']['invalid'])
        return value

    def validate_last_name(self, value):
        if not all(char.isalpha() for char in value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['last_name']['invalid'])
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['username']['exits'])
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['email']['exits'])
        return value

    def validate_password(self, value):
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+=-])[0-9a-zA-Z!@#$%^&*()_+=-]{8,}$', value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['password']['invalid'])
        return value

    def validate_confirm_password(self, value):
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+=-])[0-9a-zA-Z!@#$%^&*()_+=-]{8,}$', value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['confirm_password']['invalid'])
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'video')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user')


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    likes_name = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    comment_name = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    share_name = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    has_commented = serializers.SerializerMethodField()
    has_shared = serializers.SerializerMethodField()
    comment = CommentSerializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)
    videos = VideoSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'user', 'caption', 'created_at', 'images', 'videos', 'comment',
                  'likes_count', 'likes_name', 'comment_count', 'comment_name', 'share_count',
                  'share_name', 'has_liked', 'has_commented', 'has_shared')

    def get_likes_name(self, obj):
        obj = obj.likes.values_list('username', flat=True)
        return obj

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_comment_name(self, obj):
        obj = obj.comments.values_list('user_comment', flat=True)
        return obj

    def get_share_count(self, obj):
        return obj.shares.count()

    def get_share_name(self, obj):
        obj = obj.shares.values_list('username', flat=True)
        return obj

    def get_has_liked(self, obj):
        _user = self.context["request"].user
        return (
                _user.is_authenticated
                and
                _user.users_likes.filter(pk=obj.pk).exists()
        )

    def get_has_commented(self, obj):
        request = self.context.get('request', None)  # default value None
        if request and request.user.is_authenticated:
            return obj.comments.filter(user=request.user).exists()
        return False

    def get_has_shared(self, obj):
        _user = self.context["request"].user
        return (
                _user.is_authenticated
                and
                _user.user_share.filter(pk=obj.pk).exists()
        )

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES.getlist('images', [])
        videos_data = self.context.get('view').request.FILES.getlist('videos', [])

        post = Post.objects.create(**validated_data)

        if images_data:
            for image_data in images_data:
                Image.objects.create(post=post, image=image_data)

        if videos_data:
            for video_data in videos_data:
                Video.objects.create(post=post, video=video_data)

        return post
