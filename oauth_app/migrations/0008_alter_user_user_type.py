# Generated by Django 4.1.7 on 2023-04-01 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oauth_app", "0007_alter_user_user_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_type",
            field=models.PositiveIntegerField(
                choices=[(1, "Tutor"), (2, "Student"), (3, "Administration")], default=2
            ),
        ),
    ]