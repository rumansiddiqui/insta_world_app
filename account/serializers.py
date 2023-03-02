from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'username')

    def validate_email(self, value):
        if value == "":
            raise serializers.ValidationError("email field required")
        return value

    def validate_username(self, value):
        if len(value) <= 2:
            raise serializers.ValidationError("username is too short")
        return value

    def validate_first_name(self, value):
        if value == "":
            raise serializers.ValidationError("firstname is required")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("password must be contain 8 characters")
        return value

