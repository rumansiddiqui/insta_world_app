from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
import re


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        read_only_fields = ["id"]
        extra_kwargs = {'first_name': {'required': True},
                        'last_name': {'required': True},
                        'email': {'required': True}}


    def validate_password(self, value):
        regex1 = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if len(value) < 10:
            raise serializers.ValidationError("Length of password should be more tha or equal to 10!")
        elif regex1.search(value) is None:
            raise serializers.ValidationError("Password should contain special character!")
        return make_password(value)

    #
    # def validate_email(self, value):
    #     if value == "":
    #         raise serializers.ValidationError("Email can not be empty")
    #     return value

    # def validate_first_name(self, value):
    #     if value == "":
    #         raise serializers.ValidationError("First Name should not be blank")
    #     elif len(value)<2:
    #         raise serializers.ValidationError("First Name is too short")
    #
    #     return value
    #
    # def validate_last_name(self, value):
    #     if value == "":
    #         raise serializers.ValidationError("Last Name should not be blank")
    #     elif len(value)<2:
    #         raise serializers.ValidationError("Last Name is too short")
    #     return value
