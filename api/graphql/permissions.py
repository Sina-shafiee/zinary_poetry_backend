from graphql import GraphQLError


def permissions_required(perms):
    def decorator(func):
        def wrapper(self, info, *args, **kwargs):
            user = info.context.user
            if not user.is_authenticated:
                raise GraphQLError("Authentication required")
            if not user.has_perms(perms):
                raise GraphQLError("Permission denied")
            return func(self, info, *args, **kwargs)

        return wrapper

    return decorator
