import graphene
import json
from django.contrib.auth import login

from Twitch.schema.types import UserNode, ProfileType
from Twitch.models import TwitchUser, Profile
from Twitch.functions.api import get_twitch_user, get_users
from Twitch.functions.user import create_user


class TwitchLogin(graphene.Mutation):
    user = graphene.Field(UserNode)
    profile = graphene.Field(ProfileType)
    created = graphene.Boolean()

    class Arguments:
        twitch_username = graphene.String()
        twitch_id = graphene.Int()
        email = graphene.String()

    @classmethod
    def mutate(cls, root, info, twitch_username, twitch_id, email):
        created = False

        try:
            twitch_user_obj = TwitchUser.objects.get(twitch_id=twitch_id)
        except TwitchUser.DoesNotExist:
            twitch_user_obj = get_twitch_user(twitch_id=twitch_id)

        try:
            profile = Profile.objects.get(twitch_user=twitch_user_obj)
            user = profile.user
        except Profile.DoesNotExist:
            user, profile = create_user(username=twitch_username, email=email, twitch_user=twitch_user_obj)
            created = True

        login(info.context, user)

        return cls(user=user, profile=profile, created=created)


class SetUserLoyalty(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        payload = graphene.String()

    @classmethod
    def mutate(cls, root, info, payload):
        parsed_payload = json.loads(payload)

        existing_twitch_users = list(TwitchUser.objects.all().values_list('login', flat=True))
        new_twitch_users = []
        all_users = []

        for user in parsed_payload:
            all_users.append(user)
            if user.lower() not in existing_twitch_users:
                new_twitch_users.append(user)

        success = get_users(new_twitch_users)

        updated_list = []
        if success:
            user_objects = TwitchUser.objects.filter(login__in=all_users)
            for user in user_objects:
                user.loyalty_points = parsed_payload[user.login]['points']
                user.minutes_watched = parsed_payload[user.login]['minutes']
                updated_list.append(user)

        if len(updated_list) > 0:
            TwitchUser.objects.bulk_update(updated_list, ['loyalty_points', 'minutes_watched'])

        return cls(success=True)
