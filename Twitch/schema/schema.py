import graphene

from Twitch.schema.types import TwitchUserType
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

    @staticmethod
    def resolve_twitch_user(self, info, **kwargs):
        return TwitchUser.objects.get(login__iexact=kwargs.get('username'))

    @staticmethod
    def resolve_leaderboard(self, info, **kwargs):
        metric = kwargs.get('metric')
        return TwitchUser.objects.filter(bot=False).order_by(f'-{metric}')[:30]

