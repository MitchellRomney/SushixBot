import graphene

from Twitch.schema.types import TwitchUserType, GlobalStatisticsType
from Twitch.models import *


class Query(object):
    twitch_user = graphene.Field(
        TwitchUserType,
        username=graphene.String()
    )

    leaderboard = graphene.List(
        TwitchUserType,
        metric=graphene.String()
    )

    statistics = graphene.Field(
        GlobalStatisticsType
    )

    @staticmethod
    def resolve_twitch_user(self, info, **kwargs):
        return TwitchUser.objects.get(login__iexact=kwargs.get('username'))

    @staticmethod
    def resolve_leaderboard(self, info, **kwargs):
        metric = kwargs.get('metric')
        return TwitchUser.objects.filter(bot=False).order_by(f'-{metric}')[:30]

    @staticmethod
    def resolve_statistics(self, info, **kwargs):
        from Twitch.models import TwitchChatMessage, TwitchUser

        user = TwitchUser.objects.get(display_name='ItsSushix')
        meep_count = TwitchChatMessage.objects.filter(message__icontains='meep').count()
        follower_count = user.follower_count
        subscriber_count = user.subscriber_count
        view_count = user.view_count
        messages_count = TwitchChatMessage.objects.all().count()

        return GlobalStatisticsType(
            meep_count=meep_count,
            follower_count=follower_count,
            subscriber_count=subscriber_count,
            view_count=view_count,
            messages_count=messages_count
        )

