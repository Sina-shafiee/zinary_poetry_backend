import graphene
from graphene_django import DjangoObjectType

from api.graphql.scalars import Date

from ..models import Poet


class PoetType(DjangoObjectType):
    class Meta:
        model = Poet

    birth_year = graphene.Field(Date)
    death_year = graphene.Field(Date)


class PaginatedPoetType(graphene.ObjectType):
    poets = graphene.List(PoetType)
    total_pages = graphene.Int(required=True)
    current_page = graphene.Int(required=True)
