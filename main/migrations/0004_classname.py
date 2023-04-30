# Generated by Django 4.1.7 on 2023-04-30 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_classdescription_professors"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClassName",
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
                (
                    "class_mnen",
                    models.CharField(default="no class mnemonic", max_length=100),
                ),
                (
                    "class_name",
                    models.CharField(default="no class name", max_length=100),
                ),
            ],
        ),
    ]
