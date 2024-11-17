import graphene

from apps.poem.graphql.schema import PoemQuery, PoemMutation
from apps.poet.graphql.schema import PoetQuery, PoetMutation
from apps.collection.graphql.schema import CollectionQuery, CollectionMutation
from apps.verse.graphql.schema import VerseQuery


class Query(PoemQuery, PoetQuery, CollectionQuery, VerseQuery, graphene.ObjectType):
    pass


class Mutation(PoemMutation, PoetMutation, CollectionMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
