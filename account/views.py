from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status, serializers

from account.models import Profile, Post
from account.serializers import SignUpSerializers, SignInSerializers, ProfileSerializers, \
    PostSerializers
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin, RetrieveModelMixin
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# class ChangePasswordApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
#                         DestroyModelMixin, RetrieveModelMixin):
#     serializer_class = ChangePasswordSerializer
#     queryset = User.objects.all()


class SignUpApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                DestroyModelMixin, RetrieveModelMixin):
    serializer_class = SignUpSerializers
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.data)
            token = get_tokens_for_user(user)
            return Response({
                "token": token
            })
        return Response(serializer.errors)


class SignInApi(GenericViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = SignInSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    # http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("invalid username and password")
            return Response({
                "data": serializer.data,
                'message': "Successfully Logged In",
            }, status=status.HTTP_200_OK)
        # return Response({
        #     'data': serializer.errors,
        #     'message': "No such user found. Register First!",
        # }, status=status.HTTP_404_NOT_FOUND)


class ProfileApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                 DestroyModelMixin, RetrieveModelMixin):
    serializer_class = ProfileSerializers
    queryset = Profile.objects.all()


class PostApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
              DestroyModelMixin, RetrieveModelMixin):
    serializer_class = PostSerializers
    queryset = Post.objects.all()

    # def create(self, request, *args, **kwargs):
    #     print (request.data['images'], "=================")
    #     context = request.data['images']
    #     serializer = self.get_serializer(data=request.data, context={'image': context})
    #     print (serializer)
    #     user = serializer.is_valid()
    #     serializer.save()
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
