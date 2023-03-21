from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from post.models import Post
from post.serializers.post_serializers import UserFollowPostSerializer, UserPostSerializer


# Create your views here.


class UserFollowerPost(GenericViewSet, ListModelMixin):
    """View to get post of the users followed by user"""
    queryset = Post
    serializer_class = UserFollowPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        follower_post = self.request.user.profile.follow.all()
        return Post.objects.filter(user__in=follower_post)


class AllUserPost(GenericViewSet, ListModelMixin):
    """View to get post of all user"""
    queryset = Post.objects.all()
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated]


class UserPost(GenericViewSet, CreateModelMixin, ListModelMixin, UpdateModelMixin):
    """View to get, update and create post of login user"""

    queryset = Post
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     """ Override perform_create method to make
    #     sure the post is posted by the login user"""
    #     serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['user'] != request.user:
            return Response({'error': 'You cannot post for another user.'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



