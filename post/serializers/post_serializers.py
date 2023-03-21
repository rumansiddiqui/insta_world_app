

from post.models import Post
from .User_post_serializer import UserPostSerializer


class UserFollowPostSerializer(UserPostSerializer):
    """ Serializer for showing post of the follower user follow"""

    class Meta:
        model = Post
        fields = '__all__'
        # read_only_fields = ['user', 'likes', 'created_on', 'updated_on', 'comments',
        #                     'like_count', 'comment_count', 'has_liked']
