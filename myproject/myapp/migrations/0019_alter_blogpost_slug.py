# Generated by Django 4.2.3 on 2023-08-05 11:10

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_alter_blogpost_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=True, populate_from='title', unique=True),
        ),
    ]
