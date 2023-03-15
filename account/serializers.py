from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
import re

from account.models import Post, Profile


class UserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=20, min_length=3, required=True)
    last_name = serializers.CharField(max_length=20, min_length=3, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=20, min_length=8, required=True, write_only=True)
    confirm_password = serializers.CharField(max_length=20, min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'confirm_password')

    def validate_password(self, value):
        regex1 = re.compile('[@_!#$%^&*()<>?/}{~:]')
        if regex1.search(value) is None:
            raise serializers.ValidationError("Password should contain special character!")
        return value

    def validate(self, data):
        """
            Object level validation to check weather the given field exist or not and to match passwords
        """
        email = data.get('email')
        password = data.get('password')
        c_password = data.get('confirm_password')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists!")
        if password != c_password:
            raise serializers.ValidationError("Password and confirm password does not match!")
        return data

    def create(self, validated_data):
        """
            create function to create validated user data
        """
        return User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


class UserLogInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password")


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(max_length=20, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password does not match!")
        user.password = make_password(password)
        user.save()
        return data


class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserPostSerializer(serializers.ModelSerializer):
    media = serializers.FileField(max_length=50)
    caption = serializers.CharField(max_length=100)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_has_liked(self, obj):
        if obj.user in obj.likes.all():
            return True
        return False

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    # def create(self, validated_data):
    #     user = User.objects.get(id=validated_data['user'])
    #     likes = User.objects.filter()
    #     return Post.objects.create(
    #         user=user,
    #         media=validated_data['media'],
    #         caption=validated_data['caption'],
    #         has_liked=validated_data['has_liked'],
    #         likes=validated_data['password'],
    #         comments=validated_data['password'],
    #         created_on=validated_data['password']
    #     )


class UserProfileSerializer(serializers.ModelSerializer):
    # post = UserPostSerializer(many=True, required=False, read_only=True)
    # post = serializers.ReadOnlyField(source='user')
    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'bio', 'follow']
