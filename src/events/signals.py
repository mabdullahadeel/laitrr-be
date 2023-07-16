from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import UserFollow
from .models import Event, EventFollower


@receiver(post_save, sender=Event)
def create_event_follower(sender, instance: Event, created, **kwargs):
    """Summary
    When an event is created, create event followers for the owner's followers
    By default, all the followers of the owner will follow the event based
    on their preferences.
    """
    if not created:
        return

    bulk_create = []
    owner_followers = UserFollow.objects.filter(user=instance.owner)
    for follower in owner_followers:
        alert_preference = follower.event_alerts.all().first()
        follower_interested = (
            alert_preference.all_events
            or instance.type in alert_preference.event_types.all()
        )
        if not follower_interested:
            continue

        bulk_create.append(
            EventFollower(
                event=instance,
                follower=follower.follower,
                alert_preference=alert_preference,
            )
        )

    EventFollower.objects.bulk_create(bulk_create, batch_size=1000)
