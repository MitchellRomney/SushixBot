from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from ItsSushix.schema import schema
from Twitch import views as TwitchViews


urlpatterns = [
    path('', admin.site.urls),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('twitch/followers', TwitchViews.followers, name='twitch_followers'),
    path('twitch/subscriptions', TwitchViews.subscriptions, name='twitch_subscriptions')
]
