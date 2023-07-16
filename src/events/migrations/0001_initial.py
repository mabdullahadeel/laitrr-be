# Generated by Django 4.2.1 on 2023-07-15 23:14

import core.db
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import events.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=core.db.generate_db_id,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("resource_url", models.URLField(blank=True, null=True)),
                ("start_date", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
                "db_table": "events",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="EventAlertPreference",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=core.db.generate_db_id,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("all_events", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Event Alert Preference",
                "verbose_name_plural": "Event Alert Preferences",
                "db_table": "event_alert_preferences",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="EventType",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=core.db.generate_db_id,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("heading", models.CharField(max_length=255, unique=True)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Event Type",
                "verbose_name_plural": "Event Types",
                "db_table": "event_types",
                "ordering": ["-create_at"],
            },
        ),
        migrations.CreateModel(
            name="EventFollower",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=core.db.generate_db_id,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "alert_preference",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_followers",
                        to="events.eventalertpreference",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers",
                        to="events.event",
                    ),
                ),
                (
                    "follower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_following",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Event Follower",
                "verbose_name_plural": "Event Followers",
                "db_table": "event_followers",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="EventAnnouncement",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=core.db.generate_db_id,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="announcements",
                        to="events.event",
                    ),
                ),
            ],
            options={
                "verbose_name": "Event Announcement",
                "verbose_name_plural": "Event Announcements",
                "db_table": "event_announcements",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddField(
            model_name="eventalertpreference",
            name="event_types",
            field=models.ManyToManyField(
                blank=True, related_name="event_alerts", to="events.eventtype"
            ),
        ),
        migrations.AddField(
            model_name="eventalertpreference",
            name="user_follow",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="event_alerts",
                to="users.userfollow",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="type",
            field=models.ForeignKey(
                default=events.models.EventType.default_event_type,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="events",
                to="events.eventtype",
            ),
        ),
    ]
