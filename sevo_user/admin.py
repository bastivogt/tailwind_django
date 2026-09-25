from django.contrib import admin

from sevo_user import models


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username", 
        "email", 
        "first_name", 
        "last_name", 
        "is_staff"
    ]
    search_fields = [
        "username", 
        "email", 
        "first_name", 
        "last_name"
    ]
    list_filter = [
        "is_staff", 
        "is_superuser", 
        "is_active"
    ]


admin.site.register(models.User, UserAdmin)