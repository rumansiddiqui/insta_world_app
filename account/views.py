from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, serializers
from rest_framework.authentication import BasicAuthentication
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    ListModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from account.models import Post, Profile
from account.serializers import UserRegisterSerializer, UserLogInSerializer, UserChangePasswordSerializer, \
    DeleteUserSerializer, UserPostSerializer, UserProfileSerializer, UserFollowPostSerializer, UserSerializer
from account.utils import get_tokens_for_user


class UserLogIn(GenericViewSet, CreateModelMixin):
    """View for login user"""
    queryset = User.objects.all()
    serializer_class = UserLogInSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):

        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("No such user found. Register First!")
            user_token = get_tokens_for_user(user)

            return Response({'token': user_token,
                             "data": serializer.data,
                             'message': "Successfully Logged In",
                             }, status=status.HTTP_200_OK)
        return Response({
            'data': serializer.errors}, status=status.HTTP_404_NOT_FOUND)


class UserRegister(GenericViewSet, CreateModelMixin):
    """View to register user"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.validated_data)
            return Response({"message": "User created successfully"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePassword(GenericViewSet, UpdateModelMixin):
    """View to change password of the user"""
    queryset = User
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        queryset = self.request.user
        return queryset

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("password")):
                return Response({"password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            if request.data.get("new_password") != request.data.get("confirm_password"):
                return Response({"password": "Password and confirm password does not match!"},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(request.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data, context={'user': request.user})
    #     if serializer.is_valid(raise_exception=True):
    #         return Response({"message": "Password changed successfully"},
    #                         status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(GenericViewSet, DestroyModelMixin):
    """View for deleting user by admin user only"""
    queryset = User.objects.all()
    serializer_class = DeleteUserSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]


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


class AllUserPost(GenericViewSet, ListModelMixin):
    """View to get post of all user"""
    queryset = Post.objects.all()
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated]


class UserProfile(GenericViewSet, CreateModelMixin, ListModelMixin, UpdateModelMixin):
    """View to get, update and create user profile"""
    queryset = Profile
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)

    # def perform_create(self, serializer):
    #     """ Override perform_create method to make
    #     sure the post is posted by the login user"""
    #     serializer.save(user=self.request.user)


class UserFollowerPost(GenericViewSet, ListModelMixin):
    """View to get post of the users followed by user"""
    queryset = Post
    serializer_class = UserFollowPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        follower_post = self.request.user.profile.follow.all()
        return Post.objects.filter(user__in=follower_post)


class UserView(GenericViewSet, ListModelMixin):
    """View to get post of the users followed by user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]