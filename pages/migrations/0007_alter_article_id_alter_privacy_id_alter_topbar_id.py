# Generated by Django 4.2.1 on 2023-09-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0006_article_is_published"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="privacy",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="topbar",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
