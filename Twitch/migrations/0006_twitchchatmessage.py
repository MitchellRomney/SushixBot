# Generated by Django 3.0.1 on 2019-12-29 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Twitch', '0005_twitchuser_minutes_watched'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitchChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('twitch_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TwitchChatMessage_TwitchUsers', to='Twitch.TwitchUser')),
            ],
        ),
    ]
