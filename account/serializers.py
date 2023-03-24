import re
from django.contrib.auth.models import User
from rest_framework import serializers, request
from rest_framework.exceptions import ValidationError
from account.models import Profile, Post, Image, Video, Comment


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_password', 'old_password')


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
            raise ValidationError("Your password must contain at least 1 number, 1 uppercase, 1 lowercase,"
                                  " 1 special character and at least 8 or more characters .")
        return value


class SignInSerializers(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileSerializers(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()

    def get_followers(self, obj: Profile):
        return obj.followers.count()

    def get_followings(self, obj: Profile):
        return obj.followings.count()

    def get_post_count(self, obj: Profile):
        return obj.post.count()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'followers', 'followings', 'profile_pic', 'bio', 'post_count')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'video')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_active', 'is_staff', 'last_login', 'is_superuser', 'date_joined',
                   'groups', 'user_permissions']


class PostSerializers(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    has_saved = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, required=False)
    videos = VideoSerializer(many=True, required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = ['likes', 'comments', 'saved_by']

    def get_comment_count(self, obj: Post):
        return obj.comments.count()

    def get_likes_count(self, obj: Post):
        return obj.likes.count()

    # def get_has_liked(self, obj: Post):
    #     user: User = self.context["request"].user
    #     return user.is_authenticated and user in obj.likes.all()
    #
    def get_has_liked(self, obj: Post) -> bool:
        user: User = self.context["request"].user
        return user.is_authenticated and user.users_likes.filter(pk=obj.pk).exists()

    def get_has_saved(self, obj: Post) -> bool:
        user: User = self.context["request"].user
        return user.is_authenticated and user.saved_posts.filter(pk=obj.pk).exists()

    def create(self, validated_data):
        images_data = self.context.get('request').FILES.getlist('images', [])
        videos_data = self.context.get('request').FILES.getlist('videos', [])
        comment_data = self.initial_data.getlist('comments', [])

        post = Post.objects.create(**validated_data, user=self.context['request'].user)

        images = []
        videos = []
        comments = []

        for image_data in images_data:
            img = Image.objects.create(image=image_data)
            images.append(img)
        post.images.set(images)

        for video_data in videos_data:
            vid = Video.objects.create(video=video_data)
            videos.append(vid)
        post.videos.set(videos)

        for com_data in comment_data:
            com = Comment.objects.create(text=com_data, user_id=self.context["request"].user.id)
            comments.append(com)
        post.comments.set(comments)
        post.save()

        return post


class UserFollowersPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class UserPostLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(PostSerializers):
    class Meta:
        model = Post
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    videos = VideoSerializer(many=True, required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = ['likes', 'comments', 'saved_by']


class PostSavedSerializer(PostSerializers):
    user = UserSerializer(read_only=True)
    pass


class PostLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = ['likes', 'comments', 'saved_by']
