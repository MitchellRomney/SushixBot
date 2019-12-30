from django.contrib import admin
from django.contrib.auth.models import Group
from Twitch.models import *


class TwitchUserAdmin(admin.ModelAdmin):
    model = TwitchUser

    list_display = (
        'twitch_id',
        'bot',
        'display_name',
        'loyalty_points',
        'minutes_watched',
        'broadcaster_type',
        'view_count',
        'follower_count',
        'subscriber_count',
        'date_created'
    )


class GameAdmin(admin.ModelAdmin):
    model = Game

    list_display = (
        'game_id',
        'name'
    )


class TwitchVideoAdmin(admin.ModelAdmin):
    model = TwitchVideo

    list_display = (
        'twitch_id',
    )


class StreamMinuteFrameAdmin(admin.ModelAdmin):
    model = StreamMinuteFrame

    list_display = (
        'date_created',
        'chatters_count',
        'viewers',
        'live',
    )


class TwitchChatMessageAdmin(admin.ModelAdmin):
    model = TwitchChatMessage

    list_display = (
        'id',
        'twitch_user',
        'short_message',
        'timestamp'
    )

    list_select_related = (
        'twitch_user',
    )

    readonly_fields = (
        'twitch_user',
        'message',
        'timestamp',
        'date_modified',
        'date_created',
    )


admin.site.register(TwitchUser, TwitchUserAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(TwitchVideo, TwitchVideoAdmin)
admin.site.register(StreamMinuteFrame, StreamMinuteFrameAdmin)
admin.site.register(TwitchChatMessage, TwitchChatMessageAdmin)
admin.site.unregister(Group)
