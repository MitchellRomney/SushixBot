import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from graphql_jwt.utils import jwt_encode, jwt_payload

from Twitch.models import TwitchUser, Profile, TwitchChatMessage


class TwitchUserType(DjangoObjectType):
    messages_count = graphene.Int()

    class Meta:
        model = TwitchUser

    def resolve_messages_count(self, info):
        return TwitchChatMessage.objects.filter(twitch_user=self).count()


class UserType(DjangoObjectType):
    class Meta:
        model = User


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class UserNode(DjangoObjectType):
    token = graphene.String()

    class Meta:
        model = get_user_model()
        filter_fields = [
            'username',
        ]

    def resolve_token(self, info, **kwargs):
        if info.context.user != self:
            return None

        payload = jwt_payload(self)
        return jwt_encode(payload)


class GlobalStatisticsType(graphene.ObjectType):
    meep_count = graphene.Int()
    follower_count = graphene.Int()
    subscriber_count = graphene.Int()
    view_count = graphene.Int()
    messages_count = graphene.Int()
