from rest_framework import serializers
from django.contrib.auth.models import User
import re
from account.models import Post, Profile


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer to Register user"""
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
    """Serializer to Login user"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password")


class UserChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer for changing user password"""
    new_password = serializers.CharField(max_length=20, write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(max_length=20, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['password', 'new_password', 'confirm_password']


class DeleteUserSerializer(serializers.ModelSerializer):
    """Serializer to delete user for User model"""
    class Meta:
        model = User
        fields = '__all__'


class UserPostSerializer(serializers.ModelSerializer):
    """Serializer for Post Model"""
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    # user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Post
        fields = '__all__'
        # read_only_fields = ['user', 'likes', 'created_on', 'updated_on', 'comments',
        #                     'like_count', 'comment_count', 'has_liked']

    def get_has_liked(self, obj: Post) -> bool:
        """Check if user likes post or not"""
        user: User = self.context["request"].user
        print(user)
        return (
                user.is_authenticated
                and user.post_likes.filter(pk=obj.pk).exists()
        )

    def get_like_count(self, obj: Post) -> int:
        """Give like count of the post"""
        return obj.likes.count()

    def get_comment_count(self, obj: Post) -> int:
        """Give comment count of the post"""
        return obj.comments.count()


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer for Profile model """
    post = UserPostSerializer(many=True, read_only=True, source='user.post_set')
    follow_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'bio', 'follow_count', 'following_count', 'post']
        # read_only_fields = ['user', 'follow_count', 'following_count']

    def get_follow_count(self, obj: Profile) -> int:
        """Give follow count of the user"""
        return obj.follow.count()

    def get_following_count(self, obj: Profile) -> int:
        """Give following count of the user"""
        return obj.user.user_follow.count()


class UserFollowPostSerializer(UserPostSerializer):
    """ Serializer for showing post of the follower user follow"""
    class Meta:
        model = Post
        fields = '__all__'
        # read_only_fields = ['user', 'likes', 'created_on', 'updated_on', 'comments',
        #                     'like_count', 'comment_count', 'has_liked']


class AllUserPostSerializer(serializers.ModelSerializer):
    """ Serializer to show all user post"""
    class Meta:
        model = Post
        fields = '__all__'
        # read_only_fields = ['user', 'likes', 'created_on', 'updated_on', 'comments',
        #                     'like_count', 'comment_count', 'has_liked']
