# Generated by Django 4.1.5 on 2023-03-26 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClassList",
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
                ("class_id", models.CharField(default="cl id", max_length=10)),
                ("class_name", models.CharField(default="cl name", max_length=100)),
                ("available_tutors", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="View",
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
            ],
        ),
        migrations.CreateModel(
            name="Item",
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
                ("tutor_first_name", models.CharField(default="first", max_length=30)),
                ("tutor_last_name", models.CharField(default="last", max_length=30)),
                (
                    "classlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.classlist"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ClassDatabase",
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
                ("class_id", models.CharField(default="no class id", max_length=10)),
                (
                    "class_mnen",
                    models.CharField(default="no class mnemonic", max_length=100),
                ),
                (
                    "class_name",
                    models.CharField(default="no class name", max_length=100),
                ),
                (
                    "professors",
                    models.CharField(default="no professor", max_length=100),
                ),
                ("available_tutors", models.BooleanField(default=False)),
                (
                    "tutors",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auth.group",
                    ),
                ),
            ],
        ),
    ]
