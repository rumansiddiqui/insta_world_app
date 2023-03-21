from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status, serializers
from account.models import Profile, Post, Image, Video
from account.serializers import SignUpSerializers, SignInSerializers, ProfileSerializers, \
    PostSerializers, ChangePasswordSerializer, UserFollowersPostSerializer, \
    PostSavedSerializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin, RetrieveModelMixin
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class ChangePasswordApi(GenericViewSet, UpdateModelMixin):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': [serializer.data]
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                DestroyModelMixin, RetrieveModelMixin):
    serializer_class = SignUpSerializers
    queryset = User.objects.all()


class SignInApi(GenericViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = SignInSerializers
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("invalid username and password")
            token = get_tokens_for_user(user)
            return Response({
                "token": token,
                "data": serializer.data,
                'message': "Successfully Logged In",
            }, status=status.HTTP_200_OK)
        return Response({
            'data': serializer.errors,
            'message': "No such user found. Register First!",
        }, status=status.HTTP_404_NOT_FOUND)


class ProfileApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                 DestroyModelMixin, RetrieveModelMixin):
    serializer_class = ProfileSerializers
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]


class PostApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
              DestroyModelMixin, RetrieveModelMixin):
    serializer_class = PostSerializers
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            for image in request.FILES.getlist('image'):
                image = Image(image=image)
                image.save()
                post.image.add(image)
                post.save()
            for video in request.FILES.getlist('video'):
                video = Video(video=video)
                video.save()
                post.video.add(video)
                post.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=400)

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user)


class AllUserPost(GenericViewSet, ListModelMixin):
    serializer_class = PostSerializers
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]


class UserFollowersPostApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                           DestroyModelMixin, RetrieveModelMixin):
    serializer_class = UserFollowersPostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post

    def get_queryset(self):
        posts = self.request.user.profile.followers.all()
        return Post.objects.filter(user__in=posts)


class UserPostLikeApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                      DestroyModelMixin, RetrieveModelMixin):
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]
    queryset = Post

    def get_queryset(self):
        user = self.request.user
        return user.users_likes.all()


class PostsSavedAPIView(GenericViewSet, ListModelMixin):
    serializer_class = PostSavedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.saved_posts.all()


# class CommentApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
#                  DestroyModelMixin, RetrieveModelMixin):
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Comment
#
#     def get_queryset(self):
#         user = self.request.user
#         # comments = Comment.object.filter(comment=user)
#         post = Post.objects.filter(comments__user=user)
#         return post

