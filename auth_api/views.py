from django.conf import settings
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework import (
    views,
    generics,
    response,
    permissions,
    authentication,
    status,
)

from api.utils.success_response import rest_success_response
from .serializers import UserSerializer, LoginSerializer


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return rest_success_response(data=UserSerializer(user).data)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        logout(request)
        return response.Response()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(self.request, user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return rest_success_response(data=response.data)


class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = "pk"
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return rest_success_response(data=serializer.data)
        return Response(None, status=status.HTTP_200_OK)
