from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer


# Create your views here.
class SignUpAPI(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()


def sign_up(request):
    render(request, 'signup.html')
