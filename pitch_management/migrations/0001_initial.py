# Generated by Django 4.1.1 on 2022-10-15 20:39

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("username", models.CharField(max_length=30, unique=True)),
                ("first_name", models.CharField(max_length=300)),
                ("last_name", models.CharField(max_length=300)),
                ("address", models.CharField(max_length=300)),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=200)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("last_login", models.DateTimeField(auto_now_add=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("staff", models.BooleanField(default=False)),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("object", django.db.models.manager.Manager()),
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Pitch",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=300, unique=True)),
                ("size", models.CharField(max_length=5)),
                ("price", models.CharField(max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("pitch_name", models.CharField(max_length=300)),
                ("pitch_price", models.CharField(max_length=10)),
                ("pitch_size", models.CharField(max_length=20)),
                (
                    "timeslot",
                    models.IntegerField(
                        choices=[
                            (0, "08:00 - 09:00"),
                            (1, "09:00 - 10:00"),
                            (2, "10:00 - 11:00"),
                            (3, "11:00 - 12:00"),
                            (4, "12:00 - 13:00"),
                            (5, "13:00 - 14:00"),
                            (6, "14:00 - 15:00"),
                            (7, "15:00 - 16:00"),
                            (8, "16:00 - 17:00"),
                            (9, "17:00 - 18:00"),
                            (10, "18:00 - 19:00"),
                            (11, "19:00 - 20:00"),
                            (12, "20:00 - 21:00"),
                            (13, "21:00 - 22:00"),
                            (14, "22:00 - 23:00"),
                        ]
                    ),
                ),
                ("date", models.DateField(help_text="YYYY-MM-DD")),
                ("time", models.TimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "pitch_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pitch_management.pitch",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
