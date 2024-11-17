import graphene
from .types import PoemType
from .models import Poem


class PoemQuery(graphene.ObjectType):
    poems = graphene.List(PoemType)
    poem = graphene.Field(PoemType, id=graphene.Int())

    @staticmethod
    def resolve_poems(*args, **kwargs):
        return Poem.objects.all()

    @staticmethod
    def resolve_poem(*args, **kwargs):
        return Poem.objects.get(id=kwargs.get("id"))
