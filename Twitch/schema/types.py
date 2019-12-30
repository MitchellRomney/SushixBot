from graphene_django.types import DjangoObjectType
import graphene
from Twitch.models import TwitchUser


class TwitchUserType(DjangoObjectType):
    class Meta:
        model = TwitchUser


class GlobalStatisticsType(graphene.ObjectType):
    meep_count = graphene.Int()
    follower_count = graphene.Int()
    subscriber_count = graphene.Int()
    view_count = graphene.Int()
    messages_count = graphene.Int()
