import graphene

from apps.poem.graphql.schema import PoemQuery
from apps.poet.graphql.schema import PoetQuery


class Query(PoemQuery, PoetQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
