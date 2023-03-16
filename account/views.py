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
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import Post, Profile
from account.serializers import UserRegisterSerializer, UserLogInSerializer, UserChangePasswordSerializer, \
    DeleteUserSerializer, UserPostSerializer, UserProfileSerializer, AllUserPostSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.


class UserLogIn(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserLogInSerializer
    http_method_names = ['post']

    # permission_classes = [IsAuthenticated]

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
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']
    # permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.validated_data)
            # user_token = get_tokens_for_user(user)
            return Response({"message": "User created successfully"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePassword(GenericViewSet, UpdateModelMixin):
    # queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    # http_method_names = ['patch']
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
    queryset = User.objects.all()
    serializer_class = DeleteUserSerializer
    # http_method_names = ['delete']
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]



class UserPost(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
               DestroyModelMixin):
    # queryset = Post.objects.all()
    serializer_class = UserPostSerializer
    # http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    # def create(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         user = serializer.create(serializer.validated_data)
    #         return Response({"data": serializer.data, "message": "Post created successfully"},
    #                         status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user)

class AllUserPost(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
               DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = AllUserPostSerializer
    # http_method_names = ['post']
    permission_classes = [IsAuthenticated]


class UserProfile(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                  DestroyModelMixin):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer



