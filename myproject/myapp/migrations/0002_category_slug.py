# Generated by Django 4.2.3 on 2023-07-27 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
    ]