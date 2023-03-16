# Generated by Django 4.1.7 on 2023-03-09 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oauth_app", "0005_alter_user_user_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.PositiveIntegerField(
                choices=[(2, "Student"), (1, "Tutor")], default=2
            ),
        ),
    ]
