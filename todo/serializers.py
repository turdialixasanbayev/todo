from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError as DjangoValidationError

from .models import (
    Profile,
    ToDo
)

from .hashids import encode_id


User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        write_only=True,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="User with this email already exists"
            )
        ]
    )
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    repeat_password = serializers.CharField(write_only=True, required=True, min_length=8)
    remember_me = serializers.BooleanField(write_only=True, required=True)

    def validate_email(self, value):
        return value.lower().strip()

    def validate(self, data):
        try:
            validate_password(data["password"])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        if data["password"] != data["repeat_password"]:
            raise serializers.ValidationError({
                "repeat_password": "Passwords do not match"
            })

        return data

    def create(self, validated_data):
        validated_data.pop("repeat_password")
        validated_data.pop("remember_me")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    remember_me = serializers.BooleanField(write_only=True, required=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials"})
        data["user"] = user
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, write_only=True)


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)


class MyProfileModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "email",
            "full_name",
            "image",
            "bio",
        ]


class ProfileUpdateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'full_name',
            'image',
            'bio'
        ]


class ToDoModelSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    user = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = ToDo
        fields = [
            'id',
            'user',
            'priority',
            'title',
            'description',
            'image',
            'completed',
            'due_date',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def get_id(self, obj):
        return encode_id(obj.id)
