from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError


User = get_user_model()


class RegisterAPISerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    repeat_password = serializers.CharField(write_only=True, required=True, min_length=8)
    remember_me = serializers.BooleanField(write_only=True, required=True)

    def validate(self, data):
        try:
            validate_password(data["password"])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        if data["password"] != data["repeat_password"]:
            raise serializers.ValidationError({
                "password": "Passwords do not match"
            })

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({
                "email": "User with this email already exists"
            })

        return data

    def create(self, validated_data):
        validated_data.pop("repeat_password")
        validated_data.pop("remember_me")
        user = User.objects.create_user(**validated_data)
        return user


class LoginAPISerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    remember_me = serializers.BooleanField(write_only=True, required=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials"})
        data["user"] = user
        return data


class LogoutAPISerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, write_only=True)


class MeAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email'
        ]


class DeleteAccountAPISerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
