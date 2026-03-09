from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (
    register_view,
    login_view,
    logout_view,
    delete_account_view,
    my_profile_view,
    profile_update_view,
    ToDoModelViewSet
)


app_name = 'todo'


router = DefaultRouter()

router.register(r'todos', ToDoModelViewSet, basename='todo')


urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("auth/register/", register_view, name="register"),
    path("auth/login/", login_view, name="login"),
    path("auth/logout/", logout_view, name="logout"),
    path("auth/delete-account/", delete_account_view, name="delete-account"),
    path("auth/my-profile/", my_profile_view, name="my-profile"),
    path("auth/profile-update/", profile_update_view, name="profile-update"),

    path('viewsets/', include(router.urls)),
]
