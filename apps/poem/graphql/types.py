from graphene_django import DjangoObjectType

from ..models import Poem


class PoemType(DjangoObjectType):
    class Meta:
        model = Poem
