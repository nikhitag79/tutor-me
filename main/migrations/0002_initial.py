# Generated by Django 3.2.18 on 2023-04-30 20:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='textmessages',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='textmessages',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='request',
            name='actual_event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_request', to='main.event'),
        ),
        migrations.AddField(
            model_name='request',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='student_request', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='request',
            name='tutor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tutor_request', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='classlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.classlist'),
        ),
        migrations.AddField(
            model_name='event',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='tutor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tutor_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classdatabase',
            name='tutors',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
    ]
