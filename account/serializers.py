from rest_framework import serializers
from django.contrib.auth.models import User
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
    new_password = serializers.CharField(max_length=20, write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(max_length=20, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['password', 'new_password', 'confirm_password']


class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
         = '__all__'


class UserPostSerializer(serializers.ModelSerializer):
    like_cofieldsunt = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_has_liked(self, obj: Post) -> bool:
        user: User = self.context["request"].user
        print(user)
        return (
            user.is_authenticated
            and user.post_likes.filter(pk=obj.pk).exists()
        )

    def get_like_count(self, obj: Post) -> int:
        return obj.likes.count()

    def get_comment_count(self, obj: Post) -> int:
        return obj.comments.count()


class UserProfileSerializer(serializers.ModelSerializer):
    # post = UserPostSerializer(many=True, required=False, read_only=True)
    follow_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password does not match!")
        user.password = make_password(password)
        user.save()
        return data
    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'bio', 'follow_count', 'following_count']

    def get_follow_count(self, obj):
        return obj.follow.count()

    def get_following_count(self, obj):
        return obj.user.user_follow.count()


class AllUserPostSerializer(UserPostSerializer):
    pass

