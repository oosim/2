# Generated by Django 4.2.16 on 2024-12-23 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tap", "0011_alter_farm_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="farm",
            name="owner",
            field=models.CharField(max_length=100),
        ),
    ]