# Generated by Django 4.2.1 on 2023-07-18 02:48

import core.db
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="VerficationToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("identifier", models.CharField(max_length=255)),
                ("token", models.CharField(max_length=255, unique=True)),
                ("expires", models.DateTimeField()),
            ],
            options={
                "verbose_name": "verification token",
                "verbose_name_plural": "verification tokens",
                "db_table": "verification_tokens",
                "unique_together": {("identifier", "token")},
            },
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=core.db.generate_db_id,
                        editable=False,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("expires", models.DateTimeField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sessions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "session",
                "verbose_name_plural": "sessions",
                "db_table": "sessions",
            },
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=core.db.generate_db_id,
                        editable=False,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("type", models.CharField(max_length=50)),
                ("provider", models.CharField(max_length=50)),
                ("provider_account_id", models.CharField(max_length=255)),
                ("refresh_token", models.TextField(blank=True, null=True)),
                ("access_token", models.TextField(blank=True, null=True)),
                ("expires_at", models.PositiveIntegerField(blank=True, null=True)),
                ("token_type", models.CharField(blank=True, max_length=50, null=True)),
                ("scope", models.CharField(blank=True, max_length=255, null=True)),
                ("id_token", models.TextField(blank=True, null=True)),
                (
                    "session_state",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accounts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "account",
                "verbose_name_plural": "accounts",
                "db_table": "accounts",
                "unique_together": {("provider", "provider_account_id")},
            },
        ),
    ]
