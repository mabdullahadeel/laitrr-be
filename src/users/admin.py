from django.contrib import admin
from .models import User, UserFollow, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "id",
    ]
    ordering = ["-date_joined"]
    search_fields = ("id", "email")
    inlines = [
        ProfileInline,
    ]


admin.site.register(User, UserAdmin)
admin.site.register(UserFollow)
