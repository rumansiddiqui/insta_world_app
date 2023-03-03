from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import response
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response(" user is successfully created")
        return Response(serializer.errors)


class SignInApi(GenericViewSet, CreateModelMixin, ListModelMixin):
    serializer_class = SignInSerializers
    queryset = User.objects.all()
