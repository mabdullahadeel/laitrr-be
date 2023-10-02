from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from users.models import UserFollow, User, Profile

@receiver(post_save, sender=UserFollow)
def create_user_follow(sender, instance: UserFollow, created, **kwargs):
    if not created:
        return

    from events.models import EventAlertPreference

    EventAlertPreference.objects.create(user_follow=instance, all_events=True)


@receiver(post_save, sender=User)
def create_user_account(sender, instance: User, created, **kwargs):
    """Create an account for the user if it doesn't exist"""
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(pre_save, sender=Profile)
def delete_old_profile_image(sender, instance: Profile, **kwargs):
    """Delete old profile image if it exists"""
    try:
        old_image = Profile.objects.get(pk=instance.pk).profile_image
        if old_image:
            old_image.delete(save=False)
    except Profile.DoesNotExist:
        pass