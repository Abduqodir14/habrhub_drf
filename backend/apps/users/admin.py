from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserNetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_display_links = ("id", "username")
