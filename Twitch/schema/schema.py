import graphene
from django.contrib.auth.models import User
from django.db.models import Count, F

from Twitch.schema.types import TwitchUserType, GlobalStatisticsType, ProfileType, UserType
from Twitch.schema.mutations import TwitchLogin, SetUserLoyalty
from Twitch.models import TwitchUser, Profile, TwitchChatMessage


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

    user = graphene.Field(
        UserType,
        user_id=graphene.Int(),
        username=graphene.String()
    )

    profile = graphene.Field(
        ProfileType,
        user_id=graphene.Int()
    )

    @staticmethod
    def resolve_user(self, info, **kwargs):
        return User.objects.get(id=kwargs.get('user_id')) if kwargs.get('user_id') is not None else \
            User.objects.get(username=kwargs.get('username'))

    @staticmethod
    def resolve_profile(self, info, **kwargs):
        return Profile.objects.get(user__id=kwargs.get('user_id'))

    @staticmethod
    def resolve_twitch_user(self, info, **kwargs):
        return TwitchUser.objects.get(login__iexact=kwargs.get('username'))

    @staticmethod
    def resolve_leaderboard(self, info, **kwargs):
        metric = kwargs.get('metric')
        if metric == 'loyaltyPoints':
            return TwitchUser.objects.filter(loyalty_points__gt=0, bot=False).order_by('-loyalty_points') \
                       .exclude(display_name='ItsSushix')[:30]
        elif metric == 'minutesWatched':
            return TwitchUser.objects.filter(minutes_watched__gt=0, bot=False).order_by('-minutes_watched') \
                       .exclude(display_name='ItsSushix')[:30]
        elif metric == 'subscriptionMonths':
            return TwitchUser.objects.filter(subscription_months__gt=0, bot=False).order_by('-subscription_months') \
                       .exclude(display_name='ItsSushix')[:30]
        elif metric == 'messagesCount':
            top_list = TwitchChatMessage.objects.filter(twitch_user__bot=False).annotate(twitch_id=F('twitch_user__twitch_id')) \
                .values('twitch_id').annotate(messages=Count('id')).order_by('-messages')[:30]
            id_list = []
            for item in top_list:
                id_list.append(item['twitch_id'])
            return TwitchUser.objects.filter(twitch_id__in=id_list)

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


class Mutation(graphene.ObjectType):
    twitchLogin = TwitchLogin.Field()
    setUserLoyalty = SetUserLoyalty.Field()
