from graphene_django.types import DjangoObjectType
from Twitch.models import TwitchUser


class TwitchUserType(DjangoObjectType):
    class Meta:
        model = TwitchUser