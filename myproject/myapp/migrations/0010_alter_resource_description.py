# Generated by Django 4.2.3 on 2023-08-01 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0009_alter_resource_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="description",
            field=models.TextField(),
        ),
    ]
