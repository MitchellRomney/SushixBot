import graphene
from Twitch.schema.schema import Query


class Query(Query, graphene.ObjectType):

    pass


schema = graphene.Schema(query=Query)
