"""
this is the User post serializer file

"""
# rest framework imports
from django.contrib.auth.models import User
from rest_framework import serializers
# local imports
from account.serializers.user_serializers import UserSerializer
from post.models import Post


class UserPostSerializer(serializers.ModelSerializer):
    """Serializer for Post Model"""
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    # user = serializers.ReadOnlyField(source='user.id')
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['likes', 'comments']
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

