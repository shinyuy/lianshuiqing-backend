# Generated by Django 5.2.3 on 2025-06-27 11:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("branch", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeliveryAssignment",
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
                ("assigned_at", models.DateTimeField(auto_now_add=True)),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="branch.branch"
                    ),
                ),
            ],
        ),
    ]
