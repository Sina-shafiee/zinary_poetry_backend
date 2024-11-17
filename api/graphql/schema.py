import graphene

from apps.poem.graphql.schema import PoemQuery
from apps.poet.graphql.schema import PoetQuery
from apps.collection.graphql.schema import CollectionQuery


class Query(PoemQuery, PoetQuery, CollectionQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
