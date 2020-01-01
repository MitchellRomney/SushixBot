from django.contrib.auth.models import User

from Twitch.models import Profile


def create_user(username, email, twitch_user):
    user = User(
        username=username,
        email=email
    )
    user.set_unusable_password()
    user.save()

    profile = Profile.objects.create(
        user=user,
        twitch_user=twitch_user
    )

    return user, profile
