from datetime import timedelta

from rest_framework import generics, status, permissions
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import (
    RegisterAPISerializer,
    LoginAPISerializer,
    LogoutAPISerializer,
    MeAPISerializer,
    DeleteAccountAPISerializer,
    MyProfileAPISerializer
)
from .permissions import (
    IsAnonymous
)


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterAPISerializer
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
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "access": str(access),
                "refresh": str(refresh),
                "message": "User succesfully created.",
                "status": status.HTTP_201_CREATED
            },
            status=status.HTTP_201_CREATED
        )


register_view = RegisterAPIView.as_view()


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginAPISerializer
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
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "access": str(access),
                "refresh": str(refresh),
                "message": "User successfully logged in.",
                "status": status.HTTP_200_OK
            },
            status=status.HTTP_200_OK
        )


login_view = LoginAPIView.as_view()


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutAPISerializer
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
                {
                    "detail": "Invalid or expired token",
                    "status": status.HTTP_400_BAD_REQUEST
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Logout successful",
                "status": status.HTTP_205_RESET_CONTENT
            },
            status=status.HTTP_205_RESET_CONTENT
        )


logout_view = LogoutAPIView.as_view()


class MeAPIView(generics.RetrieveAPIView):
    serializer_class = MeAPISerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


me_view = MeAPIView.as_view()


class DeleteAccountAPIView(generics.GenericAPIView):
    serializer_class = DeleteAccountAPISerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password"]

        if not user.check_password(password):
            return Response({"detail": "Password is incorrect", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({"detail": "Account deleted successfully", "status": status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)


delete_account_view = DeleteAccountAPIView.as_view()


class MyProfileAPIView(generics.RetrieveAPIView):
    serializer_class = MyProfileAPISerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


my_profile_view = MyProfileAPIView.as_view()
