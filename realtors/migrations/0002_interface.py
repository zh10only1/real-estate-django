# Generated by Django 3.1.4 on 2022-03-05 02:01

import ckeditor.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=True)),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
