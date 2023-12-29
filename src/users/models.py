from core.db import generate_db_id
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

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

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    @property
    def name_initials(self):
        initials = ""
        if len(self.first_name) > 0:
            initials += self.first_name[0]
        if len(self.last_name) > 0:
            initials += self.last_name[0]
        if len(initials) == 0:
            initials = self.username[0:2].upper()
        
        return initials
    
    @property
    def full_name(self):
        return self.get_full_name()
    
    @staticmethod
    def get_public_safe_fields():
        return [
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "name_initials",
        ]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = "users"
    
    def get_image(self) -> str:
        return self.profile.image
    

    def __str__(self):
        return f"{self.email}"
    
    def save(self, *args, **kwargs):
        def generate_username(auto_randomize = False) -> str:
            username = ""
            if self.first_name and self.last_name:
                username = f"{self.first_name}_{self.last_name}".lower()
                if auto_randomize:
                    username += f"_{get_random_string(8)}"
            else:
                username = f"user_{get_random_string(8)}"
            
            if User.objects.filter(username=username).exists():
                return generate_username(auto_randomize=True)
            
            return username
        if not self.username:
            self.username = generate_username()
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
    
    @property
    def image(self) -> str:
        if self.profile_image:
            return self.profile_image.url
        
        return self.oauth_profile_image or None
    
    @staticmethod
    def get_public_safe_fields():
        return [
            "id",
            "profile_image",
            "oauth_profile_image"
        ]

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
