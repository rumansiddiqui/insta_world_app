import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers, request
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'username')

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

    def validate_last_name(self, value):
        if value == "":
            raise serializers.ValidationError("lastname is required")
        return value

    def validate_password(self, value):
        if re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", value) is None:
            raise ValidationError("Your password must contain at least 1 number, 1 uppercase, 1 lowercase and 1 "
                                  "special character.")
        return value

    def validate(self, data):
        if data.get("first_name").lower() == "aman" and data.get("last_name").lower() != "kumar":
            raise serializers.ValidationError("lastname must be kumar")
        return data


class SignUpSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'username', 'is_staff')

    def validate_password(self, data):
        print(data)
        if re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", data) is None:
            raise serializers.ValidationError("Your password must contain at least 1 number, 1 uppercase, 1 lowercase and 1 "
                                  "special character.")

        return data


class SignInSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    # def validate_email(self, value):
    #     if value.is_valid():


