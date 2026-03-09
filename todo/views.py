from django.shortcuts import get_object_or_404

from datetime import timedelta

from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    DeleteAccountSerializer,
    MyProfileModelSerializer,
    ProfileUpdateModelSerializer,
    ToDoModelSerializer
)
from .permissions import (
    IsAnonymous,
    IsOwner,
)
from .models import ToDo
from .hashids import decode_id


class RegisterGenericAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        remember_me = serializer.validated_data["remember_me"]

        refresh = RefreshToken.for_user(user)

        if remember_me:
            refresh.set_exp(lifetime=timedelta(days=7))

        access = refresh.access_token

        return Response(
            {
                "email": user.email,
                "access": str(access),
                "refresh": str(refresh),
                "message": "User succesfully created"
            },
            status=status.HTTP_201_CREATED
        )


register_view = RegisterGenericAPIView.as_view()


class LoginGenericAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        remember_me = serializer.validated_data["remember_me"]

        refresh = RefreshToken.for_user(user)

        if remember_me:
            refresh.set_exp(lifetime=timedelta(days=7))

        access = refresh.access_token

        return Response(
            {
                "email": user.email,
                "access": str(access),
                "refresh": str(refresh),
                "message": "User successfully logged in"
            },
            status=status.HTTP_200_OK
        )


login_view = LoginGenericAPIView.as_view()


class LogoutGenericAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT
        )


logout_view = LogoutGenericAPIView.as_view()


class DeleteAccountGenericAPIView(generics.GenericAPIView):
    serializer_class = DeleteAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password"]

        if not user.check_password(password):
            return Response(
                {"detail": "Password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.delete()
        return Response(
            {"message": "Account deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


delete_account_view = DeleteAccountGenericAPIView.as_view()


class MyProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MyProfileModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


my_profile_view = MyProfileRetrieveAPIView.as_view()


class ProfileUpdateRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


profile_update_view = ProfileUpdateRetrieveUpdateAPIView.as_view()


class ToDoModelViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoModelSerializer
    permission_classes = [IsOwner]

    filterset_fields = ['priority']
    search_fields = ['title']
    ordering_fields = ['due_date', 'created_at', 'updated_at', 'priority']
    ordering = ['-due_date']

    def get_queryset(self):
        return ToDo.objects.select_related('user').filter(
            user=self.request.user,
            is_active=True,
            completed=False
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_object(self):
        hashid = self.kwargs["pk"]
        pk = decode_id(hashid)

        return get_object_or_404(
            ToDo.objects.select_related('user').filter(
                user=self.request.user,
                is_active=True,
                completed=False
            ),
            pk=pk
        )
