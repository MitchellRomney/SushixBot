# Generated by Django 3.0.1 on 2020-01-01 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Twitch', '0006_twitchchatmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_confirmed', models.BooleanField(default=False)),
                ('archived', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('twitch_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Profile_TwitchUsers', to='Twitch.TwitchUser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Profile_Users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
