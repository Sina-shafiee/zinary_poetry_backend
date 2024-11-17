import graphene
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
