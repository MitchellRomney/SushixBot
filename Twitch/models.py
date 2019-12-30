from django.db import models
from django.template.defaultfilters import truncatechars


class TwitchUser(models.Model):
    twitch_id = models.IntegerField(unique=True, blank=False, null=False)
    login = models.CharField(max_length=255, blank=False, null=False)
    display_name = models.CharField(max_length=255, blank=False, null=False)
    type = models.CharField(max_length=255, blank=True, null=True)
    broadcaster_type = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    profile_image_url = models.URLField(blank=True, null=True)
    offline_image_url = models.URLField(blank=True, null=True)
    view_count = models.IntegerField(default=0, blank=False, null=False)
    follower_count = models.IntegerField(default=0, blank=False, null=False)
    subscriber_count = models.IntegerField(default=0, blank=False, null=False)
    loyalty_points = models.IntegerField(default=0, blank=False, null=False)
    minutes_watched = models.IntegerField(default=0, blank=False, null=False)
    bot = models.BooleanField(default=False)

    date_modified = models.DateTimeField(auto_now=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.display_name


class Game(models.Model):
    game_id = models.IntegerField(unique=True, blank=False, null=False)
    name = models.CharField(max_length=255, blank=True, null=True)

    date_modified = models.DateTimeField(auto_now=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.name or "Unknown"


class TwitchVideo(models.Model):
    twitch_id = models.IntegerField(unique=True, blank=False, null=False)
    twitch_user = models.ForeignKey(TwitchUser, related_name="TwitchVideo_TwitchUsers", on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, blank=False, null=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=False, null=False)
    published_at = models.DateTimeField(blank=False, null=False)
    url = models.URLField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    VIEWABLE_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private')
    )
    viewable = models.CharField(max_length=255, blank=False, null=False, choices=VIEWABLE_CHOICES)
    view_count = models.IntegerField(default=0, blank=False, null=False)
    language = models.CharField(max_length=255, blank=True, null=True)
    VIDEO_TYPES = (
        ('upload', 'Upload'),
        ('archive', 'Archive'),
        ('highlight', 'Highlight')
    )
    video_type = models.CharField(max_length=255, blank=False, null=False, choices=VIDEO_TYPES)
    duration = models.CharField(max_length=255, blank=False, null=False)

    date_modified = models.DateTimeField(auto_now=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.title


class StreamMinuteFrame(models.Model):
    twitch_user = models.ForeignKey(TwitchUser, related_name="StreamMinuteFrame_TwitchUsers", on_delete=models.CASCADE)
    chatters = models.ManyToManyField(TwitchUser, related_name="StreamMinuteFrame_Chatters")
    viewers = models.IntegerField(default=0, blank=False, null=False)
    live = models.BooleanField(default=False, blank=False, null=False)
    game = models.ForeignKey(Game, related_name="StreamMinuteFrame_Games", on_delete=models.SET_NULL, null=True)

    date_modified = models.DateTimeField(auto_now=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.date_created.strftime("%a %d %B %Y %H:%M")

    @property
    def chatters_count(self):
        return self.chatters.count()


class TwitchChatMessage(models.Model):
    twitch_user = models.ForeignKey(TwitchUser, related_name="TwitchChatMessage_TwitchUsers", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField()

    date_modified = models.DateTimeField(auto_now=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=False)

    @property
    def short_message(self):
        return truncatechars(self.message, 100)
