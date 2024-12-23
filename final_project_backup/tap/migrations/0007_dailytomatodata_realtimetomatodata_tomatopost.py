# Generated by Django 4.2.16 on 2024-12-23 01:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("tap", "0006_remove_post_hook_text_post_farm_owner"),
    ]

    operations = [
        migrations.CreateModel(
            name="DailyTomatoData",
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
                ("date", models.DateField()),
                ("daytime_avg_temp", models.FloatField()),
                ("nighttime_avg_temp", models.FloatField()),
                ("daytime_avg_humidity", models.FloatField()),
                ("nighttime_avg_humidity", models.FloatField()),
                ("daily_total_light", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="RealTimeTomatoData",
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
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("temperature", models.FloatField()),
                ("humidity", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="TomatoPost",
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
                ("category", models.CharField(max_length=50)),
                ("title", models.CharField(max_length=100)),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("csv_file", models.FileField(upload_to="media/")),
            ],
        ),
    ]
