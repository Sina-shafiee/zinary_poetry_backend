import math
import graphene

from api.graphql.permissions import permissions_required
from api.graphql.utils import apply_query_filters

from .types import PaginatedPoetType, PoetType
from ..models import Poet


class PoetQuery(graphene.ObjectType):
    poets = graphene.Field(
        PaginatedPoetType,
        page=graphene.Int(),
        per_page=graphene.Int(),
        q=graphene.String(description="search query"),
        sort=graphene.String(),
    )
    poet = graphene.Field(PoetType, id=graphene.Int())

    @staticmethod
    def resolve_poets(root, info, page=1, per_page=10, q=None, sort=None):
        queryset = Poet.objects.all()

        result = apply_query_filters(
            queryset=queryset,
            page=page,
            per_page=per_page,
            search=q,
            search_fields=["full_name", "biography"],  # Fields to search
            sort=sort,
        )

        return PaginatedPoetType(
            poets=result["queryset"],
            total_pages=result["total_pages"],
            current_page=result["current_page"],
        )


class CreatePoet(graphene.Mutation):
    class Arguments:
        full_name = graphene.String(required=True)
        birth_year = graphene.Date(description="format YY-MM-DD")
        death_year = graphene.Date(description="format YY-MM-DD")
        biography = graphene.String(required=True)

    poet = graphene.Field(PoetType)

    @staticmethod
    @permissions_required(["poet.add_poet"])
    def mutate(root, info, full_name, biography, birth_year=None, death_year=None):

        poet = Poet.objects.create(
            full_name=full_name,
            biography=biography,
            birth_year=birth_year,
            death_year=death_year,
        )
        return CreatePoet(poet=poet)


class UpdatePoet(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        full_name = graphene.String()
        birth_year = graphene.Date(description="format YY-MM-DD")
        death_year = graphene.Date(description="format YY-MM-DD")
        biography = graphene.String()

    poet = graphene.Field(PoetType)

    @staticmethod
    @permissions_required(["poet.change_poet"])
    def mutate(
        root, info, id, full_name=None, birth_year=None, death_year=None, biography=None
    ):
        try:
            poet = Poet.objects.get(id=id)
        except Poet.DoesNotExist:
            raise Exception("Poet not found")

        if full_name:
            poet.full_name = full_name
        if biography:
            poet.biography = biography
        if birth_year:
            poet.birth_year = birth_year
        if death_year:
            poet.death_year = death_year

        poet.save()
        return UpdatePoet(poet=poet)


class PoetMutation(graphene.ObjectType):
    create_poet = CreatePoet.Field()
    update_poet = UpdatePoet.Field()
