from django.contrib import admin

from .models import CustomUser, Profile

admin.site.site_header = "ToDo Admin Dashboard"
admin.site.site_title = "ToDo Admin Dashboard"
admin.site.index_title = "Welcome to ToDo Admin Dashboard"
admin.site.empty_value_display = "None"


admin.site.register(CustomUser)
admin.site.register(Profile)
