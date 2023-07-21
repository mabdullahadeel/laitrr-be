from __future__ import annotations
from core.db import generate_db_id
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from auth.models import Account, Session


def profile_image_path(instance: "Profile", filename: str):
    return f"profile_images/{instance.user.id}.{filename.split('.')[-1]}"


class User(AbstractUser):
    id = models.CharField(
        primary_key=True, default=generate_db_id, editable=False, max_length=36
    )
    email = models.EmailField(unique=True)
    email_verified = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    profile: "Profile"
    following: "UserFollow"
    followers: "UserFollow"
    accounts: list[Account]
    sessions: Optional[list[Session]]

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = "users"

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@")[0].replace(".", "_")
        if not self.password:
            self.set_password(get_random_string(32))
        super().save(*args, **kwargs)


class Profile(models.Model):
    id = models.CharField(
        primary_key=True, default=generate_db_id, editable=False, max_length=36
    )
    profile_image = models.ImageField(
        upload_to=profile_image_path, blank=True, null=True
    )
    oauth_profile_image = models.URLField(blank=True, null=True)
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        db_table = "profiles"

    def __str__(self) -> str:
        return self.id


class UserFollow(models.Model):
    id = models.CharField(
        primary_key=True, default=generate_db_id, editable=False, max_length=36
    )
    # user who is being followed
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    # user who is following
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "user follow"
        verbose_name_plural = "user follows"
        db_table = "user_follow"
        unique_together = ("user", "follower")

    def __str__(self):
        return f"{self.follower} ----> {self.user}"

    def save(self, *args, **kwargs):
        if self.user == self.follower:
            raise Exception("You cannot follow yourself")
        super().save(*args, **kwargs)
