from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile, ToDo

admin.site.site_header = "ToDo Admin Dashboard"
admin.site.site_title = "ToDo Admin Dashboard"
admin.site.index_title = "Welcome to ToDo Admin Dashboard"
admin.site.empty_value_display = "Nonea"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "is_staff")
    filter_horizontal = ("groups", "user_permissions")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide"), "fields": ("email", "usable_password", "password1", "password2")})
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)
    autocomplete_fields = ('user',)


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'priority',
        'title',
        'image',
        'completed',
        'due_date',
        'is_active',
    )
    search_fields = ('title',)
    autocomplete_fields = ('user',)
    list_filter = (
        'priority',
        'is_active',
        'completed',
        'due_date'
    )
    list_editable = (
        "completed",
        "priority",
        'is_active',
    )
    list_display_links = ("user", "title")
