from graphene_django import DjangoObjectType

from ..models import Poet


class PoetType(DjangoObjectType):
    class Meta:
        model = Poet
