from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name')

    def validate_password(self, value):
        return make_password(value)
