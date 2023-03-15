import re
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers, request
from rest_framework.exceptions import ValidationError

from account.models import Profile, Post, Images, Videos, Comment


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
#     confirm_password = serializers.CharField(required=True)
#
#     class Meta:
#         model = User
#         fields = ('new_password', 'confirm_password', 'old_password')


class SignUpSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'username', 'is_staff')

    def create(self, validated_data):
        return User.objects.create_user(
            first_name=validated_data['first_name'], last_name=validated_data['last_name'],
            email=validated_data['email'], username=validated_data['username'],
            password=validated_data['password'])

    def validate_email(self, value):
        if value == "":
            raise serializers.ValidationError("email field required")
        return value

    def validate_username(self, value):
        if len(value) <= 2:
            raise serializers.ValidationError("username is too short")
        return value

    def validate_first_name(self, value):
        if value == "":
            raise serializers.ValidationError("firstname is required")
        return value

    def validate_last_name(self, value):
        if value == "":
            raise serializers.ValidationError("lastname is required")
        return value

    def validate_password(self, value):
        if re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", value) is None:
            raise ValidationError("Your password must contain at least 1 number, 1 uppercase, 1 lowercase and 1 "
                                  "special character.")
        return value


class SignInSerializers(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'followers', 'followings')


class ImageSerializer(serializers.ModelSerializer):
    images = serializers.FileField()

    class Meta:
        model = Images
        fields = ('id', 'images')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = ('id', 'videos')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'comment')


class PostSerializers(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    likes_name = serializers.SerializerMethodField()
    has_comment = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, required=False)
    videos = VideoSerializer(many=True, required=False)
    comment = CommentSerializer(many=True, required=False)

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_has_liked(self, obj):
        for user in obj.likes.all():
            if user == obj.user:
                return True
        return False

    def get_has_comment(self, obj):
        for user in obj.comments.all():
            if user == obj.user:
                return True
        return False

    def get_likes_name(self, obj):
        obj = obj.likes.values_list('username', flat=True)
        return obj

    class Meta:
        model = Post
        exclude = ['likes', 'comments']

    # def create(self, validated_data, *args, **kwargs):
    #     print(args, "----------------")
    #     print(kwargs, "++++++++++++")
    #     print(validated_data, "////////////////////")
    #     data = self.context['image']
    #     my_model = Post.objects.create(**validated_data)
    #     for image_data in data:
    #         from django.core.files.images import ImageFile
    #         # m = Model1.objects.create()
    #         # m.f1 = ImageFile(open("1.png", "rb"))
    #         # m.save()
    #         image = Images.objects.create()
    #         image.images = image_data
    #         image.save()
    #         my_model.images.add(image)
    #     return my_model
