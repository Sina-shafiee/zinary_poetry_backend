from graphene_django import DjangoObjectType

from ..models import Collection


class CollectionType(DjangoObjectType):
    class Meta:
        model = Collection
