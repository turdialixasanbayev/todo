from django.db import models

from django.conf import settings

from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    full_name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="profiles/%Y/%m/%d/", blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email}'s profile"


class ToDo(models.Model):

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='todos'
    )
    priority = models.CharField(
        max_length=15,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    title = models.CharField(max_length=225)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="todos/%Y/%m/%d/", blank=True, null=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todos"

    def __str__(self):
        return self.title
