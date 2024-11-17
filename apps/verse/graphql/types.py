from graphene_django import DjangoObjectType

from ..models import Verse


class VerseType(DjangoObjectType):
    class Meta:
        model = Verse
