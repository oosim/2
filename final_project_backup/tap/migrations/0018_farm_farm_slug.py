# Generated by Django 4.2.16 on 2024-12-24 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tap", "0017_recipe"),
    ]

    operations = [
        migrations.AddField(
            model_name="farm",
            name="farm_slug",
            field=models.SlugField(
                allow_unicode=True, blank=True, max_length=200, null=True, unique=True
            ),
        ),
    ]
