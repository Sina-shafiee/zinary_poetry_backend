import graphene
from .types import CollectionType
from ..models import Collection


class CollectionQuery(graphene.ObjectType):
    collections = graphene.List(CollectionType)
    collection = graphene.Field(CollectionType, id=graphene.Int(required=True))

    @staticmethod
    def resolve_collections(*args, **kwargs):
        return Collection.objects.all()

    @staticmethod
    def resolve_collection(*args, **kwargs):
        return Collection.objects.get(id=kwargs.get("id"))
