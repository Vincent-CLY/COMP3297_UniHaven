# Generated by Django 5.1.7 on 2025-04-02 09:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Accommodation",
            fields=[
                (
                    "accommodation_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=100)),
                ("type", models.CharField(max_length=100)),
                ("is_available", models.BooleanField(default=True)),
                ("owner_details", models.CharField(max_length=100)),
                ("available_from", models.DateTimeField()),
                ("available_to", models.DateTimeField()),
                ("bed_num", models.IntegerField()),
                ("bedroom_num", models.IntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("distance_from_campus", models.FloatField(blank=True, null=True)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                ("geoAddress", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("user_id", models.IntegerField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("email", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="CEDARSStaff",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="app.user",
                    ),
                ),
                ("staff_id", models.CharField(max_length=20, unique=True)),
                ("staff_department", models.CharField(max_length=100)),
            ],
            bases=("app.user",),
        ),
        migrations.CreateModel(
            name="HKUStudent",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="app.user",
                    ),
                ),
                ("HKU_ID", models.CharField(max_length=20, unique=True)),
            ],
            bases=("app.user",),
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "notification_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("type", models.CharField(max_length=100)),
                ("notification_content", models.TextField()),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.user"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("reservation_id", models.AutoField(primary_key=True, serialize=False)),
                ("reservation_date", models.DateTimeField()),
                ("check_in_date", models.DateTimeField()),
                ("check_out_date", models.DateTimeField()),
                ("is_cancelled", models.BooleanField(default=False)),
                (
                    "accommodation_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.accommodation",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.user"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CancelledReservation",
            fields=[
                (
                    "cancellation_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.user"
                    ),
                ),
                (
                    "reservation_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.reservation",
                    ),
                ),
            ],
        ),
    ]
