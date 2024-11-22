import graphene

from api.graphql.permissions import permissions_required

from apps.collection.models import Collection
from apps.poet.models import Poet

from ..models import Poem
from .types import PoemType


class PoemQuery(graphene.ObjectType):
    poems = graphene.List(PoemType)
    poem = graphene.Field(PoemType, id=graphene.Int())

    @staticmethod
    def resolve_poems(*args, **kwargs):
        return Poem.objects.all()

    @staticmethod
    def resolve_poem(*args, **kwargs):
        return Poem.objects.get(id=kwargs.get("id"))


class CreatePoem(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year_written = graphene.Date()
        poet_id = graphene.Int(required=True)
        collection_id = graphene.Int(required=True)

    poem = graphene.Field(PoemType)

    @staticmethod
    @permissions_required(["poem.add_poem"])
    def mutate(root, info, title, poet_id, collection_id, year_written=None):
        poet = Poet.objects.get(id=poet_id)
        collection = Collection.objects.get(id=collection_id)

        poem = Poem.objects.create(
            title=title, year_written=year_written, poet=poet, collection=collection
        )

        return CreatePoem(poem=poem)


class UpdatePoem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        year_written = graphene.Date()
        poet_id = graphene.Int()
        collection_id = graphene.Int()

    poem = graphene.Field(PoemType)

    @staticmethod
    @permissions_required(["poem.change_poem"])
    def mutate(
        root, info, id, title=None, year_written=None, poet_id=None, collection_id=None
    ):
        try:
            poem = Poem.objects.get(id=id)
        except Poem.DoesNotExist:
            raise Exception("Poem not found")

        if title:
            poem.title = title
        if year_written:
            poem.year_written = year_written
        if poet_id:
            poem.poet = Poet.objects.get(id=poet_id)
        if collection_id:
            poem.collection = Collection.objects.get(id=collection_id)

        poem.save()

        return UpdatePoem(poem=poem)


class PoemMutation(graphene.ObjectType):
    create_poem = CreatePoem.Field()
    update_poem = UpdatePoem.Field()
