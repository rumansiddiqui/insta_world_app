from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, \
    UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView

from account.serializers import UserSerializer


# Create your views here.
class UserModelApi(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UpdateDeleteApi(GenericAPIView, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


