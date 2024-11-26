from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("auth/", include("auth_api.urls")),
    path("file/", include("apps.file.urls")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
