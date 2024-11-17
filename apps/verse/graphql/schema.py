import graphene

from api.graphql.permissions import permissions_required
from apps.poem.models import Poem

from .types import VerseType
from ..models import Verse


class VerseQuery(graphene.ObjectType):
    verses = graphene.List(VerseType)
    verse = graphene.Field(VerseType, id=graphene.Int(required=True))

    @staticmethod
    def resolve_verses(*args, **kwargs):
        return Verse.objects.all()

    @staticmethod
    def resolve_verse(*args, **kwargs):
        return Verse.objects.get(id=kwargs.get("id"))


class CreateVerse(graphene.Mutation):
    class Arguments:
        order = graphene.Int(required=True)
        first_hemistich = graphene.String(required=True)
        second_hemistich = graphene.String(required=True)
        poem_id = graphene.Int(required=True)

    verse = graphene.Field(VerseType)

    @staticmethod
    @permissions_required(["verse.add_verse"])
    def mutate(root, info, order, first_hemistich, second_hemistich, poem_id):
        try:
            poem = Poem.objects.get(id=poem_id)
        except Poem.DoesNotExist:
            raise Exception("Poem not found")

        verse = Verse.objects.create(
            order=order,
            first_hemistich=first_hemistich,
            second_hemistich=second_hemistich,
            poem=poem,
        )
        return CreateVerse(verse=verse)


class UpdateVerse(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        order = graphene.Int()
        first_hemistich = graphene.String()
        second_hemistich = graphene.String()

    verse = graphene.Field(VerseType)

    @staticmethod
    @permissions_required(["verse.change_verse"])
    def mutate(root, info, id, order=None, first_hemistich=None, second_hemistich=None):
        try:
            verse = Verse.objects.get(id=id)
        except Verse.DoesNotExist:
            raise Exception("Verse not found")

        if order:
            verse.order = order
        if first_hemistich:
            verse.first_hemistich = first_hemistich
        if second_hemistich:
            verse.second_hemistich = second_hemistich

        verse.save()
        return UpdateVerse(verse=verse)


class VerseMutation(graphene.ObjectType):
    create_verse = CreateVerse.Field()
    update_verse = UpdateVerse.Field()
