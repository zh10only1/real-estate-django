# Generated by Django 4.2.1 on 2024-02-15 08:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0008_translation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="translation",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
