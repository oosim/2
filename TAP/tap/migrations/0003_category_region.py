# Generated by Django 4.2.16 on 2024-12-15 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tap", "0002_post_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="region",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
