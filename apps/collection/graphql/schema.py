import graphene

from api.graphql.permissions import permissions_required
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


class CreateCollection(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        type = graphene.String(required=True)
        description = graphene.String()

    collection = graphene.Field(CollectionType)

    @staticmethod
    @permissions_required(["collection.add_collection"])
    def mutate(root, info, title, type, description=None):
        collection = Collection.objects.create(
            title=title,
            type=type,
            description=description if description else "",
        )
        return CreateCollection(collection=collection)


class UpdateCollection(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        type = graphene.String()

    collection = graphene.Field(CollectionType)

    @staticmethod
    @permissions_required(["collection.change_collection"])
    def mutate(root, info, id, title=None, description=None, type=None):
        try:
            collection = Collection.objects.get(id=id)
        except Collection.DoesNotExist:
            raise Exception("Collection not found")

        if title:
            collection.title = title
        if type:
            collection.type = type
        if description:
            collection.description = description

        collection.save()
        return UpdateCollection(collection=collection)


class CollectionMutation(graphene.ObjectType):
    create_collection = CreateCollection.Field()
    update_collection = UpdateCollection.Field()
