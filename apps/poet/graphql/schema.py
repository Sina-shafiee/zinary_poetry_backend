import graphene
from .types import PoetType
from ..models import Poet


class PoetQuery(graphene.ObjectType):
    poets = graphene.List(PoetType)
    poet = graphene.Field(PoetType, id=graphene.Int())

    @staticmethod
    def resolve_poets(*args, **kwargs):
        return Poet.objects.all()

    @staticmethod
    def resolve_poet(*args, **kwargs):
        return Poet.objects.get(id=kwargs.get("id"))
