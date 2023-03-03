from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from account.serializers import UserSerializer, SignUpSerializers, SignInSerializers
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


class SignInApi(GenericViewSet):
    serializer_class = SignInSerializers
    queryset = User.objects.all()




