import graphene

from apps.poem.graphql.schema import PoemQuery, PoemMutation
from apps.poet.graphql.schema import PoetQuery
from apps.collection.graphql.schema import CollectionQuery
from apps.verse.graphql.schema import VerseQuery


class Query(PoemQuery, PoetQuery, CollectionQuery, VerseQuery, graphene.ObjectType):
    pass


class Mutation(PoemMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
