from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from account.models import Profile, Post
from account.serializers import UserSerializer, SignUpSerializers, SignInSerializers, ProfileSerializers, \
    PostSerializers
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin, RetrieveModelMixin


# Create your views here.
class UserModelApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                   DestroyModelMixin, RetrieveModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SignUpApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                DestroyModelMixin, RetrieveModelMixin):
    serializer_class = SignUpSerializers
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response("user is successfully created")
        return Response(serializer.errors)


class SignInApi(GenericViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = SignInSerializers
    queryset = User.objects.all()


class ProfileApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
                 DestroyModelMixin, RetrieveModelMixin):
    serializer_class = ProfileSerializers
    queryset = Profile.objects.all()


class PostApi(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin,
              DestroyModelMixin, RetrieveModelMixin):
    serializer_class = PostSerializers
    queryset = Post.objects.all()

    # def list(self, request, *args, **kwargs):
    #     post = self.get_queryset().select_related()
    #     serializer = self.get_serializer(instance=post, many=True)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
