from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, serializers, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, \
    UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from account.serializers import UserRegisterSerializer, UserLogInSerializer


# class StudentLogin(viewsets.ModelViewSet):
#     queryset = User
#     serializer_class = UserLogInSerializer
#     http_method_names = ['post']
#
#     def get_queryset(self):
#         """
#         The get_queryset method returns a queryset of Student_Info Model objects.
#         """
#         return User.objects.filter()
#
#     def create(self, request, *args, **kwargs):
#         """
#         Allows only valid user to login.
#         """
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             # user = serializer.validated_data['user']
#             return Response(status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# Create your views here.

class UserLogIn(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserLogInSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            # user = serializer.validated_data['user']
            return Response({
                "data": serializer.data,
                'message': "Successfully Logged In",
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UserRegister(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin,
                   UpdateModelMixin, DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response("User created successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
