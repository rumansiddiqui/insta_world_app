from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, \
    UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account.serializers import UserSerializer


# Create your views here.

class UserView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin,
               UpdateModelMixin, DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class UserViewRUD(GenericViewSet, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
