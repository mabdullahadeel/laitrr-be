from django.contrib import admin

# from auth.models import Account
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

class AccountAdmin(admin.ModelAdmin):
    search_fields = ("id", "user__email")
    list_display = [
        "id",
        "user",
    ]


admin.site.register(User, UserAdmin)
admin.site.register(UserFollow)
admin.site.register(Profile)
