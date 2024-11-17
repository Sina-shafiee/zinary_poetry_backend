import graphene

from apps.poem.graphql.schema import PoemQuery


class Query(PoemQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
